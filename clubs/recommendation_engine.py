# -*- coding: utf-8 -*-
"""
社团智能推荐系统 - 推荐算法引擎
包含：加权匹配、协同过滤、混合推荐等核心算法
针对实际Club模型字段进行了适配
"""

from collections import defaultdict
import logging
import math
from typing import List, Dict, Tuple, Optional

from django.db.models import Q, Count, Avg
from django.contrib.auth.models import User
from django.core.cache import cache

from clubs.models import Club, Membership, CrossSchoolEvent
from clubs.recommendation_models import (
    StudentProfile, InterestTag, StudentInterest,
    ClubTag, UserBehavior, RecommendationResult, 
    SimilarityMatrix, ClubRecommendationData
)

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """
    推荐引擎核心类
    整合多种推荐算法，提供统一的推荐接口
    """
    
    # 算法权重配置
    ALGORITHM_WEIGHTS = {
        'weighted': 0.40,      # 加权匹配
        'cf_user': 0.30,      # 用户协同过滤
        'cf_item': 0.30,      # 物品协同过滤
    }
    
    # 推荐结果数量
    TOP_N = 10
    
    # 缓存时间（秒）
    CACHE_TIMEOUT = 3600  # 1小时
    
    def __init__(self, user: User):
        self.user = user
        self.student_profile = self._get_student_profile()
        self.user_id = user.id
    
    def _get_student_profile(self) -> Optional[StudentProfile]:
        """获取学生档案"""
        try:
            return self.user.student_profile
        except StudentProfile.DoesNotExist:
            return None
    
    def _get_user_clubs(self) -> List[int]:
        """获取用户已加入的社团ID列表"""
        return list(
            Membership.objects.filter(
                user=self.user
            ).values_list('club_id', flat=True)
        )
    
    def _get_user_behavior_clubs(self) -> List[int]:
        """获取用户有过行为的社团ID列表"""
        return list(
            UserBehavior.objects.filter(
                user=self.user,
                club_id__isnull=False
            ).values_list('club_id', flat=True)
        )
    
    def _get_club_tags(self, club: Club) -> List[str]:
        """获取社团的标签列表"""
        return list(
            ClubTag.objects.filter(club=club).values_list('tag__name', flat=True)
        )
    
    def _get_club_member_count(self, club: Club) -> int:
        """获取社团成员数量"""
        return club.members.count()
    
    def _get_club_activity_count(self, club: Club) -> int:
        """获取社团活动数量"""
        return club.cross_events.count()
    
    def _get_club_active_time(self, club: Club) -> Dict:
        """获取社团活跃时间"""
        try:
            return club.recommendation_data.active_time or {}
        except ClubRecommendationData.DoesNotExist:
            return {}
    
    def get_recommendations(self, limit: int = None, force_refresh: bool = False) -> List[Dict]:
        """
        获取推荐列表（主入口）
        
        Args:
            limit: 返回数量限制
            force_refresh: 是否强制刷新缓存
        
        Returns:
            推荐社团列表，每项包含社团信息和推荐分数
        """
        if limit is None:
            limit = self.TOP_N
        
        # 检查缓存
        cache_key = f'recommend:{self.user_id}'
        if not force_refresh:
            cached_result = cache.get(cache_key)
            if cached_result:
                return cached_result[:limit]
        
        # 检查是否有学生档案
        if not self.student_profile:
            logger.warning(f"User {self.user_id} has no student profile, returning popular clubs")
            return self._get_popular_clubs(limit)
        
        # 计算推荐
        recommendations = self._compute_hybrid_recommendations()
        
        # 排序并截取
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        result = recommendations[:limit]
        
        # 存入数据库（可选，用于分析）
        self._save_recommendation_results(result)
        
        # 存入缓存
        cache.set(cache_key, result, self.CACHE_TIMEOUT)
        
        return result
    
    def _compute_hybrid_recommendations(self) -> List[Dict]:
        """
        混合推荐算法
        结合加权匹配、用户协同过滤、物品协同过滤
        """
        # 获取所有社团
        all_clubs = Club.objects.all()
        user_clubs = self._get_user_clubs()
        
        recommendations = []
        
        for club in all_clubs:
            # 跳过已加入的社团
            if club.id in user_clubs:
                continue
            
            # 1. 加权匹配分数
            weighted_score = self._compute_weighted_match(club)
            
            # 2. 用户协同过滤分数
            cf_user_score = self._compute_user_cf_score(club)
            
            # 3. 物品协同过滤分数
            cf_item_score = self._compute_item_cf_score(club)
            
            # 4. 混合总分
            total_score = (
                weighted_score * self.ALGORITHM_WEIGHTS['weighted'] +
                cf_user_score * self.ALGORITHM_WEIGHTS['cf_user'] +
                cf_item_score * self.ALGORITHM_WEIGHTS['cf_item']
            )
            
            # 5. 生成推荐理由
            reasons = self._generate_reasons(club, weighted_score, cf_user_score, cf_item_score)
            
            recommendations.append({
                'club': club,
                'club_id': club.id,
                'club_name': club.name,
                'club_category': club.category,
                'club_tags': self._get_club_tags(club),
                'score': round(total_score, 2),
                'weighted_score': round(weighted_score, 2),
                'cf_user_score': round(cf_user_score, 2),
                'cf_item_score': round(cf_item_score, 2),
                'reasons': reasons,
                'member_count': self._get_club_member_count(club),
                'activity_count': self._get_club_activity_count(club),
            })
        
        return recommendations
    
    def _compute_weighted_match(self, club: Club) -> float:
        """
        加权匹配算法
        基于学生特征与社团特征的匹配度计算
        """
        if not self.student_profile:
            return 50.0  # 默认分数
        
        profile = self.student_profile
        weights = {
            'major': 0.35,
            'category': 0.35,
            'tags': 0.20,
            'active_time': 0.10,
        }
        
        # 1. 专业相关度 (0-100)
        major_score = self._calculate_major_score(club)
        
        # 2. 分类偏好匹配度 (0-100)
        category_score = self._calculate_category_score(club)
        
        # 3. 标签匹配度 (0-100)
        tags_score = self._calculate_tags_score(club)
        
        # 4. 活跃时间匹配度 (0-100)
        active_time_score = self._calculate_active_time_score(club)
        
        # 加权求和
        total = (
            major_score * weights['major'] +
            category_score * weights['category'] +
            tags_score * weights['tags'] +
            active_time_score * weights['active_time']
        )
        
        return min(100, max(0, total))
    
    def _calculate_major_score(self, club: Club) -> float:
        """计算专业相关度"""
        if not self.student_profile or not self.student_profile.major:
            return 50.0
        
        major = self.student_profile.major
        desc = club.description.lower() if club.description else ''
        
        # 专业相关关键词映射
        major_keywords = {
            '计算机': ['技术', '编程', '软件', 'AI', '算法', '信息', '计算机'],
            '软件': ['开发', '编程', '工程', '软件'],
            '数学': ['建模', '统计', '分析', '算法', '数学'],
            '物理': ['工程', '技术', '实验', '物理'],
            '化学': ['实验', '材料', '化工', '化学'],
            '生物': ['生命', '医学', '健康', '生物'],
            '经济': ['商业', '金融', '管理', '市场', '经济'],
            '管理': ['商业', '组织', '领导', '企业', '管理'],
            '法律': ['法规', '政策', '正义', '法律'],
            '外语': ['交流', '翻译', '国际', '文化', '外语'],
            '艺术': ['创意', '设计', '审美', '艺术'],
            '体育': ['运动', '健康', '竞技', '体能', '体育'],
        }
        
        # 查找专业对应的社团关键词
        for major_key, club_keywords in major_keywords.items():
            if major_key in major:
                for kw in club_keywords:
                    if kw in desc:
                        return 85.0
                return 60.0
        
        return 50.0
    
    def _calculate_category_score(self, club: Club) -> float:
        """计算分类偏好匹配度"""
        if not self.student_profile:
            return 50.0
        
        # 获取学生最感兴趣的分类
        top_interests = StudentInterest.objects.filter(
            student=self.student_profile
        ).select_related('tag').order_by('-weight')[:3]
        
        if not top_interests:
            return 50.0
        
        # 匹配度
        for interest in top_interests:
            if interest.tag.category == club.category:
                return 70.0 + interest.weight * 30.0  # 70-100
        
        return 40.0
    
    def _calculate_tags_score(self, club: Club) -> float:
        """计算标签匹配度"""
        if not self.student_profile:
            return 50.0
        
        student_tags = set(
            StudentInterest.objects.filter(
                student=self.student_profile
            ).values_list('tag__name', flat=True)
        )
        
        club_tags = set(self._get_club_tags(club))
        
        if not student_tags or not club_tags:
            return 50.0
        
        # Jaccard相似度
        intersection = len(student_tags & club_tags)
        union = len(student_tags | club_tags)
        
        if union == 0:
            return 50.0
        
        jaccard = intersection / union
        
        # 转换为0-100分数
        return jaccard * 100
    
    def _calculate_active_time_score(self, club: Club) -> float:
        """计算活跃时间匹配度"""
        if not self.student_profile or not self.student_profile.active_time:
            return 50.0
        
        club_time = self._get_club_active_time(club)
        if not club_time:
            return 50.0
        
        student_time = self.student_profile.active_time
        
        # 计算时间重叠度
        common_times = 0
        total_times = 0
        
        for period in ['morning', 'afternoon', 'evening', 'night']:
            if period in student_time and period in club_time:
                s_val = student_time.get(period, 0)
                c_val = club_time.get(period, 0)
                if s_val > 0.5 and c_val > 0.5:
                    common_times += 1
                total_times += 1
        
        if total_times == 0:
            return 50.0
        
        return (common_times / total_times) * 100
    
    def _compute_user_cf_score(self, club: Club) -> float:
        """
        用户协同过滤分数
        找到与当前用户相似的用户，看他们是否加入过该社团
        """
        # 获取相似用户
        similar_users = self._find_similar_users(limit=20)
        
        if not similar_users:
            return 50.0
        
        # 统计相似用户加入该社团的情况
        total_similarity = 0
        weighted_score = 0
        
        for user_id, similarity in similar_users:
            # 检查该相似用户是否加入了该社团
            is_member = Membership.objects.filter(
                user_id=user_id,
                club=club
            ).exists()
            
            if is_member:
                weighted_score += similarity * 100
                total_similarity += similarity
        
        if total_similarity == 0:
            return 50.0
        
        return weighted_score / total_similarity
    
    def _compute_item_cf_score(self, club: Club) -> float:
        """
        物品协同过滤分数
        找到与用户已加入社团相似的社团
        """
        user_clubs = self._get_user_clubs()
        
        if not user_clubs:
            return 50.0
        
        # 获取与该社团相似的已加入社团
        similarities = list(
            SimilarityMatrix.objects.filter(
                matrix_type='item_item',
                entity_a=club.id,
                entity_b__in=user_clubs
            ).values_list('entity_b', 'similarity')
        )
        
        if not similarities:
            # 也检查反向
            similarities = list(
                SimilarityMatrix.objects.filter(
                    matrix_type='item_item',
                    entity_b=club.id,
                    entity_a__in=user_clubs
                ).values_list('entity_a', 'similarity')
            )
        
        if not similarities:
            return 50.0
        
        # 加权平均相似度
        total_sim = sum(sim for _, sim in similarities)
        count = len(similarities)
        
        return (total_sim / count) * 100 if count > 0 else 50.0
    
    def _find_similar_users(self, limit: int = 20) -> List[Tuple[int, float]]:
        """
        找到与当前用户相似的用户
        基于用户行为的相似度计算
        """
        # 检查缓存的相似用户
        cache_key = f'similar_users:{self.user_id}'
        cached = cache.get(cache_key)
        if cached:
            return cached[:limit]
        
        # 获取当前用户的行为向量
        user_vector = self._get_user_behavior_vector()
        
        if not user_vector:
            return []
        
        # 获取与当前用户有共同行为的用户
        user_club_ids = set(self._get_user_behavior_clubs())
        
        if not user_club_ids:
            return []
        
        # 查找也对这些社团有行为的其他用户
        other_behaviors = UserBehavior.objects.filter(
            club_id__in=user_club_ids,
            user__is_active=True
        ).exclude(
            user=self.user
        ).values('user_id').annotate(
            count=Count('id')
        ).order_by('-count')[:50]
        
        similar_users = []
        for behavior in other_behaviors:
            other_user_id = behavior['user_id']
            other_vector = self._get_user_behavior_vector(other_user_id)
            
            if other_vector:
                similarity = self._cosine_similarity(user_vector, other_vector)
                if similarity > 0.1:  # 相似度阈值
                    similar_users.append((other_user_id, similarity))
        
        # 按相似度排序
        similar_users.sort(key=lambda x: x[1], reverse=True)
        
        # 缓存
        cache.set(cache_key, similar_users, self.CACHE_TIMEOUT)
        
        return similar_users[:limit]
    
    def _get_user_behavior_vector(self, user_id: int = None) -> Dict[int, float]:
        """获取用户行为向量 {社团ID: 行为权重分数}"""
        if user_id is None:
            user_id = self.user_id
        
        behaviors = UserBehavior.objects.filter(
            user_id=user_id,
            club_id__isnull=False
        ).values('club_id', 'behavior_type')
        
        vector = defaultdict(float)
        
        behavior_weights = {
            'view': 1.0,
            'like': 3.0,
            'apply': 5.0,
            'attend': 7.0,
            'rate': 8.0,
            'share': 4.0,
            'comment': 6.0,
        }
        
        for behavior in behaviors:
            club_id = behavior['club_id']
            btype = behavior['behavior_type']
            vector[club_id] += behavior_weights.get(btype, 1.0)
        
        return dict(vector)
    
    def _cosine_similarity(self, vec1: Dict, vec2: Dict) -> float:
        """计算两个向量的余弦相似度"""
        if not vec1 or not vec2:
            return 0.0
        
        # 找共同的key
        common_keys = set(vec1.keys()) & set(vec2.keys())
        
        if not common_keys:
            return 0.0
        
        # 计算点积和模长
        dot_product = sum(vec1[k] * vec2[k] for k in common_keys)
        norm1 = math.sqrt(sum(vec1[k] ** 2 for k in vec1.keys()))
        norm2 = math.sqrt(sum(vec2[k] ** 2 for k in vec2.keys()))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def _generate_reasons(self, club: Club, weighted: float, 
                         cf_user: float, cf_item: float) -> List[str]:
        """生成推荐理由"""
        reasons = []
        
        # 基于加权匹配的理由
        if weighted > 70:
            # 检查分类匹配
            if self.student_profile:
                top_interests = StudentInterest.objects.filter(
                    student=self.student_profile
                ).select_related('tag').order_by('-weight')[:1]
                
                if top_interests:
                    tag = top_interests[0].tag
                    if tag.category == club.category:
                        reasons.append(f"与你的兴趣「{tag.name}」匹配")
                
                # 检查标签重叠
                student_tags = set(
                    StudentInterest.objects.filter(
                        student=self.student_profile
                    ).values_list('tag__name', flat=True)
                )
                club_tags = set(self._get_club_tags(club))
                overlap = student_tags & club_tags
                if overlap:
                    reasons.append(f"共同标签：{', '.join(list(overlap)[:2])}")
        
        # 基于协同过滤的理由
        if cf_user > 60:
            reasons.append("与你相似的同学都在关注")
        
        if cf_item > 60:
            reasons.append("与你加入的社团风格相似")
        
        # 通用理由
        member_count = self._get_club_member_count(club)
        if member_count > 20:
            reasons.append(f"人气社团（{member_count}人）")
        
        activity_count = self._get_club_activity_count(club)
        if activity_count > 5:
            reasons.append(f"活动丰富（累计{activity_count}场活动）")
        
        # 默认理由
        if not reasons:
            reasons.append("适合你的社团")
        
        return reasons[:3]  # 最多3个理由
    
    def _save_recommendation_results(self, recommendations: List[Dict]):
        """保存推荐结果到数据库"""
        for rec in recommendations:
            RecommendationResult.objects.update_or_create(
                user=self.user,
                club_id=rec['club_id'],
                defaults={
                    'score': rec['score'],
                    'weighted_score': rec['weighted_score'],
                    'cf_user_score': rec['cf_user_score'],
                    'cf_item_score': rec['cf_item_score'],
                    'grade_score': 0,
                    'major_score': 0,
                    'category_score': 0,
                    'tags_score': 0,
                    'active_time_score': 0,
                    'reasons': rec['reasons'],
                    'algorithm': 'hybrid',
                }
            )
    
    def _get_popular_clubs(self, limit: int = 10) -> List[Dict]:
        """获取热门社团（用于无档案用户）"""
        clubs = Club.objects.annotate(
            member_count=Count('members')
        ).order_by('-member_count')[:limit]
        
        return [{
            'club': club,
            'club_id': club.id,
            'club_name': club.name,
            'club_category': club.category,
            'club_tags': self._get_club_tags(club),
            'score': 50.0,  # 默认分数
            'reasons': ['热门社团', f'{self._get_club_member_count(club)}名成员'],
            'member_count': self._get_club_member_count(club),
            'activity_count': self._get_club_activity_count(club),
        } for club in clubs]
    
    def record_feedback(self, club_id: int, feedback_type: str, reason: str = ''):
        """
        记录用户反馈
        用于优化推荐算法
        """
        club = Club.objects.get(id=club_id)
        
        # 获取推荐时的分数
        rec_result = RecommendationResult.objects.filter(
            user=self.user,
            club_id=club_id
        ).first()
        
        original_score = rec_result.score if rec_result else 0
        
        # 保存反馈
        from clubs.recommendation_models import RecommendationFeedback
        RecommendationFeedback.objects.create(
            user=self.user,
            club_id=club_id,
            feedback_type=feedback_type,
            original_score=original_score,
            reason=reason,
        )
        
        # 更新推荐结果
        if rec_result:
            rec_result.is_viewed = True
            if feedback_type == 'like':
                rec_result.is_interested = True
            elif feedback_type == 'dislike':
                rec_result.is_interested = False
            rec_result.save()
        
        # 清除缓存
        cache.delete(f'recommend:{self.user_id}')


class SimilarityCalculator:
    """
    相似度计算器
    用于离线计算用户/社团相似度矩阵
    """
    
    @staticmethod
    def compute_user_similarity_matrix():
        """
        计算用户-用户相似度矩阵
        应该定期离线执行（如每天）
        """
        logger.info("Starting user similarity matrix computation...")
        
        # 获取所有活跃用户
        users = User.objects.filter(is_active=True)
        
        # 获取所有用户的行为向量
        behavior_vectors = {}
        for user in users:
            engine = RecommendationEngine(user)
            vector = engine._get_user_behavior_vector()
            if vector:
                behavior_vectors[user.id] = vector
        
        # 计算相似度
        computed = 0
        for uid1, vec1 in behavior_vectors.items():
            for uid2, vec2 in behavior_vectors.items():
                if uid1 >= uid2:  # 避免重复
                    continue
                
                similarity = RecommendationEngine._cosine_similarity(None, vec1, vec2)
                
                if similarity > 0.1:  # 只保存有意义的相似度
                    SimilarityMatrix.objects.update_or_create(
                        matrix_type='user_user',
                        entity_a=uid1,
                        entity_b=uid2,
                        defaults={
                            'similarity': similarity,
                            'sample_size': len(set(vec1.keys()) | set(vec2.keys())),
                        }
                    )
                    computed += 1
        
        logger.info(f"Computed {computed} user similarity pairs")
        return computed
    
    @staticmethod
    def compute_item_similarity_matrix():
        """
        计算社团-社团相似度矩阵
        基于用户行为的Item-Based CF
        """
        logger.info("Starting item similarity matrix computation...")
        
        # 获取所有社团
        clubs = Club.objects.all()
        
        # 构建用户-社团矩阵
        user_club_matrix = defaultdict(set)
        
        memberships = Membership.objects.all().values('user_id', 'club_id')
        
        for m in memberships:
            user_club_matrix[m['user_id']].add(m['club_id'])
        
        if not user_club_matrix:
            logger.info("No membership data found")
            return 0
        
        # 转换为社团-用户倒排表
        club_users = defaultdict(set)
        for user, club_set in user_club_matrix.items():
            for club_id in club_set:
                club_users[club_id].add(user)
        
        # 计算社团之间的相似度
        computed = 0
        club_ids = list(club_users.keys())
        
        for i, club1_id in enumerate(club_ids):
            for club2_id in club_ids[i+1:]:
                # Jaccard相似度
                users1 = club_users[club1_id]
                users2 = club_users[club2_id]
                
                intersection = len(users1 & users2)
                union = len(users1 | users2)
                
                if union > 0:
                    similarity = intersection / union
                    
                    if similarity > 0.05:  # 只保存有意义的相似度
                        SimilarityMatrix.objects.update_or_create(
                            matrix_type='item_item',
                            entity_a=club1_id,
                            entity_b=club2_id,
                            defaults={'similarity': similarity}
                        )
                        computed += 1
        
        logger.info(f"Computed {computed} item similarity pairs")
        return computed


def get_personalized_recommendations(user: User, limit: int = 10) -> List[Dict]:
    """
    获取个性化推荐（便捷函数）
    """
    engine = RecommendationEngine(user)
    return engine.get_recommendations(limit=limit)


def refresh_user_recommendations(user: User):
    """
    刷新用户推荐（强制重新计算）
    """
    engine = RecommendationEngine(user)
    return engine.get_recommendations(force_refresh=True)
