# -*- coding: utf-8 -*-
"""
社团智能推荐系统 - API视图
提供推荐、统计、数据可视化等接口
"""

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Count, Avg, Q, Sum, F
from django.utils import timezone
import json
import logging

from clubs.models import Club, Membership, CrossSchoolEvent
from clubs.recommendation_engine import (
    RecommendationEngine, 
    get_personalized_recommendations,
    SimilarityCalculator
)
from clubs.recommendation_models import (
    StudentProfile, InterestTag, StudentInterest,
    ClubTag, UserBehavior, RecommendationResult,
    ClubRecommendationData, SimilarityMatrix
)

logger = logging.getLogger(__name__)


class RecommendationAPI(View):
    """
    社团推荐API
    GET: 获取推荐列表
    POST: 记录用户反馈
    """
    
    def get(self, request):
        """获取推荐列表"""
        if not request.user.is_authenticated:
            return JsonResponse({'code': 401, 'msg': '请先登录'})
        
        limit = int(request.GET.get('limit', 10))
        force_refresh = request.GET.get('refresh', 'false').lower() == 'true'
        
        try:
            if force_refresh:
                recommendations = RecommendationEngine(request.user).get_recommendations(
                    limit=limit, 
                    force_refresh=True
                )
            else:
                recommendations = get_personalized_recommendations(request.user, limit=limit)
            
            # 序列化
            data = []
            for rec in recommendations:
                club = rec['club'] if 'club' in rec else Club.objects.get(id=rec['club_id'])
                data.append({
                    'id': club.id,
                    'name': club.name,
                    'logo': club.logo.url if club.logo else None,
                    'category': club.category,
                    'tags': rec.get('club_tags', []),
                    'description': club.description[:100] + '...' if len(club.description) > 100 else club.description,
                    'member_count': club.member_count,
                    'activity_count': club.activity_count,
                    'score': rec['score'],
                    'score_breakdown': {
                        'weighted': rec.get('weighted_score', 0),
                        'cf_user': rec.get('cf_user_score', 0),
                        'cf_item': rec.get('cf_item_score', 0),
                    },
                    'reasons': rec.get('reasons', []),
                })
            
            return JsonResponse({
                'code': 200, 
                'msg': 'success',
                'data': data,
                'total': len(data)
            })
            
        except Exception as e:
            logger.error(f"Recommendation error: {e}")
            return JsonResponse({'code': 500, 'msg': f'推荐服务出错: {str(e)}'})
    
    def post(self, request):
        """记录推荐反馈"""
        if not request.user.is_authenticated:
            return JsonResponse({'code': 401, 'msg': '请先登录'})
        
        try:
            data = json.loads(request.body)
            club_id = data.get('club_id')
            feedback_type = data.get('feedback_type')
            reason = data.get('reason', '')
            
            if not club_id or not feedback_type:
                return JsonResponse({'code': 400, 'msg': '缺少必要参数'})
            
            # 记录反馈
            engine = RecommendationEngine(request.user)
            engine.record_feedback(club_id, feedback_type, reason)
            
            return JsonResponse({'code': 200, 'msg': '反馈已记录'})
            
        except Exception as e:
            logger.error(f"Feedback error: {e}")
            return JsonResponse({'code': 500, 'msg': str(e)})


class StudentProfileAPI(View):
    """
    学生档案API
    GET: 获取档案
    POST: 更新档案
    """
    
    def get(self, request):
        """获取学生档案"""
        if not request.user.is_authenticated:
            return JsonResponse({'code': 401, 'msg': '请先登录'})
        
        try:
            profile = request.user.student_profile
            interests = list(
                StudentInterest.objects.filter(student=profile)
                .select_related('tag')
                .values('tag__id', 'tag__name', 'tag__category', 'weight')
            )
            
            data = {
                'id': profile.id,
                'gender': profile.gender,
                'grade': profile.grade,
                'major': profile.major,
                'academy': profile.academy,
                'phone': profile.phone,
                'bio': profile.bio,
                'active_time': profile.active_time or {},
                'interests': interests,
                'avatar': profile.avatar.url if profile.avatar else None,
            }
            
            return JsonResponse({'code': 200, 'msg': 'success', 'data': data})
            
        except StudentProfile.DoesNotExist:
            return JsonResponse({
                'code': 404, 
                'msg': '请先完善个人信息',
                'data': None
            })
    
    def post(self, request):
        """更新学生档案"""
        if not request.user.is_authenticated:
            return JsonResponse({'code': 401, 'msg': '请先登录'})
        
        try:
            data = json.loads(request.body)
            
            # 获取或创建档案
            profile, created = StudentProfile.objects.get_or_create(user=request.user)
            
            # 更新字段
            if 'gender' in data:
                profile.gender = data['gender']
            if 'grade' in data:
                profile.grade = data['grade']
            if 'major' in data:
                profile.major = data['major']
            if 'academy' in data:
                profile.academy = data['academy']
            if 'phone' in data:
                profile.phone = data['phone']
            if 'bio' in data:
                profile.bio = data['bio']
            if 'active_time' in data:
                profile.active_time = data['active_time']
            
            profile.save()
            
            # 更新兴趣标签
            if 'interests' in data:
                # 删除旧标签
                StudentInterest.objects.filter(student=profile).delete()
                
                # 添加新标签
                for item in data['interests']:
                    tag_id = item.get('tag_id')
                    weight = item.get('weight', 1.0)
                    
                    if tag_id:
                        try:
                            tag = InterestTag.objects.get(id=tag_id)
                            StudentInterest.objects.create(
                                student=profile,
                                tag=tag,
                                weight=weight
                            )
                        except InterestTag.DoesNotExist:
                            pass
            
            # 清除推荐缓存
            cache.delete(f'recommend:{request.user.id}')
            
            return JsonResponse({
                'code': 200, 
                'msg': '档案更新成功',
                'data': {'profile_id': profile.id}
            })
            
        except Exception as e:
            logger.error(f"Profile update error: {e}")
            return JsonResponse({'code': 500, 'msg': str(e)})


class InterestTagsAPI(View):
    """
    兴趣标签API
    GET: 获取所有标签
    """
    
    def get(self, request):
        """获取所有标签"""
        category = request.GET.get('category')
        
        tags = InterestTag.objects.all()
        if category:
            tags = tags.filter(category=category)
        
        data = list(tags.values('id', 'name', 'category', 'description', 'heat'))
        
        return JsonResponse({
            'code': 200,
            'msg': 'success',
            'data': data
        })


class StatisticsAPI(View):
    """
    数据统计API
    提供各种统计数据
    """
    
    def get(self, request):
        """获取统计数据"""
        stat_type = request.GET.get('type', 'overview')
        
        if stat_type == 'overview':
            return self._get_overview_stats()
        elif stat_type == 'clubs':
            return self._get_club_stats()
        elif stat_type == 'activities':
            return self._get_activity_stats()
        elif stat_type == 'students':
            return self._get_student_stats()
        elif stat_type == 'heatmap':
            return self._get_activity_heatmap()
        elif stat_type == 'recommendation':
            return self._get_recommendation_stats()
        else:
            return JsonResponse({'code': 400, 'msg': '未知统计类型'})
    
    def _get_overview_stats(self):
        """总览统计"""
        total_users = User.objects.filter(is_active=True).count()
        total_clubs = Club.objects.filter(status='approved').count()
        total_activities = Activity.objects.filter(status='approved').count()
        total_participations = ActivityParticipation.objects.count()
        
        return JsonResponse({
            'code': 200,
            'msg': 'success',
            'data': {
                'total_users': total_users,
                'total_clubs': total_clubs,
                'total_activities': total_activities,
                'total_participations': total_participations,
            }
        })
    
    def _get_club_stats(self):
        """社团统计"""
        # 按分类统计
        category_stats = Club.objects.filter(
            status='approved'
        ).values('category').annotate(
            count=Count('id'),
            total_members=Sum('member_count')
        )
        
        # 热门社团
        hot_clubs = Club.objects.filter(
            status='approved'
        ).order_by('-member_count', '-view_count')[:10].values(
            'id', 'name', 'category', 'member_count', 'activity_count', 'view_count'
        )
        
        # 社团增长率（简化版，实际需要历史数据）
        growth_data = [
            {'month': '2026-01', 'count': Club.objects.filter(created_at__month=1).count()},
            {'month': '2026-02', 'count': Club.objects.filter(created_at__month=2).count()},
            {'month': '2026-03', 'count': Club.objects.filter(created_at__month=3).count()},
            {'month': '2026-04', 'count': Club.objects.filter(created_at__month=4).count()},
        ]
        
        return JsonResponse({
            'code': 200,
            'msg': 'success',
            'data': {
                'category_stats': list(category_stats),
                'hot_clubs': list(hot_clubs),
                'growth_data': growth_data,
            }
        })
    
    def _get_activity_stats(self):
        """活动统计"""
        # 按类型统计
        type_stats = Activity.objects.filter(
            status='approved'
        ).values('activity_type').annotate(
            count=Count('id'),
            avg_participants=Avg('current_participants')
        )
        
        # 热门活动
        hot_activities = Activity.objects.filter(
            status='approved'
        ).order_by('-current_participants', '-rating')[:10].values(
            'id', 'title', 'activity_type', 'current_participants', 'rating'
        )
        
        return JsonResponse({
            'code': 200,
            'msg': 'success',
            'data': {
                'type_stats': list(type_stats),
                'hot_activities': list(hot_activities),
            }
        })
    
    def _get_student_stats(self):
        """学生统计"""
        # 年级分布
        grade_stats = StudentProfile.objects.exclude(
            grade__isnull=True
        ).values('grade').annotate(count=Count('id'))
        
        # 专业分布（简化）
        major_stats = StudentProfile.objects.exclude(
            major__isnull=True
        ).values('major').annotate(
            count=Count('id')
        ).order_by('-count')[:20]
        
        # 性别分布
        gender_stats = StudentProfile.objects.exclude(
            gender__isnull=True
        ).values('gender').annotate(count=Count('id'))
        
        return JsonResponse({
            'code': 200,
            'msg': 'success',
            'data': {
                'grade_stats': list(grade_stats),
                'major_stats': list(major_stats),
                'gender_stats': list(gender_stats),
            }
        })
    
    def _get_activity_heatmap(self):
        """活动热力图数据"""
        # 按月份和星期统计活动数量
        activities = Activity.objects.filter(
            status='approved'
        ).values('start_time')
        
        # 简化统计
        month_data = [0] * 12
        weekday_data = [0] * 7
        
        for activity in activities:
            start = activity['start_time']
            if start:
                month_data[start.month - 1] += 1
                weekday_data[start.weekday()] += 1
        
        return JsonResponse({
            'code': 200,
            'msg': 'success',
            'data': {
                'monthly': month_data,
                'weekly': weekday_data,
            }
        })
    
    def _get_recommendation_stats(self):
        """推荐系统统计"""
        if not hasattr(self, 'request') or not self.request.user.is_authenticated:
            return JsonResponse({'code': 401, 'msg': '请先登录'})
        
        user = self.request.user
        
        # 用户的推荐统计
        total_recommendations = RecommendationResult.objects.filter(user=user).count()
        viewed_recommendations = RecommendationResult.objects.filter(
            user=user, 
            is_viewed=True
        ).count()
        interested_recommendations = RecommendationResult.objects.filter(
            user=user, 
            is_interested=True
        ).count()
        
        # 平均推荐分数
        avg_score = RecommendationResult.objects.filter(
            user=user
        ).aggregate(Avg('score'))
        
        return JsonResponse({
            'code': 200,
            'msg': 'success',
            'data': {
                'total_recommendations': total_recommendations,
                'viewed': viewed_recommendations,
                'interested': interested_recommendations,
                'avg_score': round(avg_score['score__avg'] or 0, 2),
                'view_rate': round(viewed_recommendations / total_recommendations * 100, 2) if total_recommendations > 0 else 0,
            }
        })


class SimilarityComputeAPI(View):
    """
    相似度矩阵计算API
    仅管理员使用
    """
    
    def post(self, request):
        """触发相似度矩阵计算"""
        if not request.user.is_authenticated or not request.user.is_staff:
            return JsonResponse({'code': 403, 'msg': '需要管理员权限'})
        
        matrix_type = request.GET.get('type', 'all')
        
        try:
            if matrix_type in ['all', 'user']:
                user_count = SimilarityCalculator.compute_user_similarity_matrix()
            
            if matrix_type in ['all', 'item']:
                item_count = SimilarityCalculator.compute_item_similarity_matrix()
            
            return JsonResponse({
                'code': 200,
                'msg': '计算完成',
                'data': {
                    'user_pairs': user_count if matrix_type in ['all', 'user'] else 0,
                    'item_pairs': item_count if matrix_type in ['all', 'item'] else 0,
                }
            })
            
        except Exception as e:
            logger.error(f"Similarity computation error: {e}")
            return JsonResponse({'code': 500, 'msg': str(e)})


class ActivityTimelineAPI(View):
    """
    活动时间线API
    获取近期活动时间线
    """
    
    def get(self, request):
        """获取活动时间线"""
        days = int(request.GET.get('days', 30))
        
        now = timezone.now()
        start_date = now - timezone.timedelta(days=days)
        
        activities = Activity.objects.filter(
            status='approved',
            start_time__gte=start_date
        ).select_related('club').order_by('start_time')[:50]
        
        data = []
        for activity in activities:
            data.append({
                'id': activity.id,
                'title': activity.title,
                'club_name': activity.club.name,
                'club_id': activity.club.id,
                'start_time': activity.start_time.strftime('%Y-%m-%d %H:%M'),
                'end_time': activity.end_time.strftime('%Y-%m-%d %H:%M'),
                'location': activity.location,
                'type': activity.activity_type,
                'participants': f'{activity.current_participants}/{activity.max_participants}' if activity.max_participants else activity.current_participants,
            })
        
        return JsonResponse({
            'code': 200,
            'msg': 'success',
            'data': data
        })


@method_decorator(csrf_exempt, name='dispatch')
class BehaviorRecordAPI(View):
    """
    用户行为记录API
    记录用户的浏览、收藏等行为
    """
    
    def post(self, request):
        """记录用户行为"""
        if not request.user.is_authenticated:
            return JsonResponse({'code': 401, 'msg': '请先登录'})
        
        try:
            data = json.loads(request.body)
            
            behavior_type = data.get('behavior_type')
            club_id = data.get('club_id')
            activity_id = data.get('activity_id')
            
            if not behavior_type:
                return JsonResponse({'code': 400, 'msg': '缺少行为类型'})
            
            # 行为权重
            behavior_weights = {
                'view': 1.0,
                'like': 3.0,
                'apply': 5.0,
                'attend': 7.0,
                'rate': 8.0,
            }
            
            # 记录行为
            UserBehavior.objects.create(
                user=request.user,
                behavior_type=behavior_type,
                club_id=club_id,
                activity_id=activity_id,
                weight=behavior_weights.get(behavior_type, 1.0),
            )
            
            # 如果是view，增加浏览次数
            if behavior_type == 'view' and club_id:
                Club.objects.filter(id=club_id).update(
                    view_count=models.F('view_count') + 1
                )
            
            # 如果是like，增加收藏次数
            if behavior_type == 'like' and club_id:
                Club.objects.filter(id=club_id).update(
                    like_count=models.F('like_count') + 1
                )
            
            return JsonResponse({'code': 200, 'msg': '行为已记录'})
            
        except Exception as e:
            logger.error(f"Behavior record error: {e}")
            return JsonResponse({'code': 500, 'msg': str(e)})


# 辅助函数
from django.db.models import Sum


def sum_values(queryset):
    """Sum helper for Django"""
    return queryset.aggregate(total=Sum('value'))['total'] or 0
