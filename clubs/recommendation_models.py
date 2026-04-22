# -*- coding: utf-8 -*-
"""
社团智能推荐系统 - 数据模型
包含学生画像、社团标签、用户行为、推荐结果等核心数据表
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import hashlib
import datetime


class StudentProfile(models.Model):
    """学生扩展信息表"""
    
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
        ('O', '其他'),
    ]
    
    GRADE_CHOICES = [
        ('1', '大一'),
        ('2', '大二'),
        ('3', '大三'),
        ('4', '大四'),
        ('5', '大五'),
        ('6', '研究生'),
        ('7', '博士'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    gender = models.CharField('性别', max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    grade = models.CharField('年级', max_length=2, choices=GRADE_CHOICES, blank=True, null=True)
    major = models.CharField('专业', max_length=100, blank=True, null=True)
    academy = models.CharField('学院', max_length=100, blank=True, null=True)
    phone = models.CharField('手机号', max_length=20, blank=True, null=True)
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True, null=True)
    bio = models.TextField('个人简介', blank=True, null=True)
    
    #活跃时间段（JSON格式：{"morning": 0.8, "afternoon": 0.3, "evening": 0.9}）
    active_time = models.JSONField('活跃时间偏好', default=dict, blank=True)
    
    # 创建时间
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'student_profile'
        verbose_name = '学生信息'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f"{self.user.username} - {self.get_grade_display() if self.grade else '未填写'}"


class InterestTag(models.Model):
    """兴趣标签表"""
    
    CATEGORY_CHOICES = [
        ('sports', '体育运动'),
        ('arts', '文艺表演'),
        ('culture', '传统文化'),
        ('academic', '学术科创'),
        ('public_welfare', '公益实践'),
        ('interest', '兴趣生活'),
    ]
    
    name = models.CharField('标签名称', max_length=50, unique=True)
    category = models.CharField('所属分类', max_length=20, choices=CATEGORY_CHOICES)
    description = models.CharField('标签描述', max_length=200, blank=True)
    heat = models.IntegerField('热度', default=0)  # 标签被选次数
    
    class Meta:
        db_table = 'interest_tag'
        verbose_name = '兴趣标签'
        verbose_name_plural = verbose_name
        ordering = ['-heat']
    
    def __str__(self):
        return self.name


class StudentInterest(models.Model):
    """学生兴趣关联表"""
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='interests')
    tag = models.ForeignKey(InterestTag, on_delete=models.CASCADE, related_name='students')
    weight = models.FloatField('兴趣权重', default=1.0)  # 0.0-1.0
    created_at = models.DateTimeField('选择时间', auto_now_add=True)
    
    class Meta:
        db_table = 'student_interest'
        verbose_name = '学生兴趣'
        verbose_name_plural = verbose_name
        unique_together = ['student', 'tag']
    
    def __str__(self):
        return f"{self.student.user.username} - {self.tag.name}"


class ClubTag(models.Model):
    """社团官方标签表"""
    
    club = models.ForeignKey('clubs.Club', on_delete=models.CASCADE, related_name='recommendation_tags')
    tag = models.ForeignKey(InterestTag, on_delete=models.CASCADE, related_name='clubs')
    weight = models.FloatField('标签权重', default=1.0)
    
    class Meta:
        db_table = 'club_tag'
        verbose_name = '社团标签'
        verbose_name_plural = verbose_name
        unique_together = ['club', 'tag']
    
    def __str__(self):
        return f"{self.club.name} - {self.tag.name}"


class UserBehavior(models.Model):
    """
    用户行为记录表
    用于协同过滤推荐算法
    """
    
    BEHAVIOR_CHOICES = [
        ('view', '浏览'),
        ('like', '收藏'),
        ('apply', '申请'),
        ('attend', '参加活动'),
        ('rate', '评分'),
        ('share', '分享'),
        ('comment', '评论'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='behaviors')
    club_id = models.IntegerField('社团ID', null=True, blank=True)
    activity_id = models.IntegerField('活动ID', null=True, blank=True)
    
    behavior_type = models.CharField('行为类型', max_length=20, choices=BEHAVIOR_CHOICES)
    
    # 行为权重（用于计算相似度）
    weight = models.FloatField('行为权重', default=1.0)
    
    # 上下文信息
    context = models.JSONField('上下文', default=dict, blank=True)
    
    created_at = models.DateTimeField('行为时间', auto_now_add=True)
    
    class Meta:
        db_table = 'user_behavior'
        verbose_name = '用户行为'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'behavior_type']),
            models.Index(fields=['club_id', 'behavior_type']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.get_behavior_type_display()}"


class RecommendationResult(models.Model):
    """
    推荐结果表
    存储离线计算或实时计算的推荐结果
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    club_id = models.IntegerField('社团ID')
    
    # 推荐分数
    score = models.FloatField('推荐分数', help_text='0-100')
    
    # 各维度分数
    grade_score = models.FloatField('年级匹配度', default=0)
    major_score = models.FloatField('专业匹配度', default=0)
    category_score = models.FloatField('分类匹配度', default=0)
    tags_score = models.FloatField('标签匹配度', default=0)
    active_time_score = models.FloatField('时间匹配度', default=0)
    cf_score = models.FloatField('协同过滤分数', default=0, help_text='协同过滤算法得分')
    
    # 推荐理由
    reasons = models.JSONField('推荐理由', default=list)
    
    # 算法来源
    algorithm = models.CharField('算法', max_length=50, 
                                 choices=[
                                     ('weighted', '加权匹配'),
                                     ('cf_user', '用户协同过滤'),
                                     ('cf_item', '物品协同过滤'),
                                     ('hybrid', '混合推荐'),
                                 ])
    
    # 是否已查看/处理
    is_viewed = models.BooleanField('是否查看', default=False)
    is_interested = models.BooleanField('是否感兴趣', null=True, blank=True)
    
    created_at = models.DateTimeField('生成时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'recommendation_result'
        verbose_name = '推荐结果'
        verbose_name_plural = verbose_name
        ordering = ['-score']
        unique_together = ['user', 'club_id']
        indexes = [
            models.Index(fields=['user', '-score']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} -> Club {self.club_id} ({self.score:.2f})"


class SimilarityMatrix(models.Model):
    """
    相似度矩阵表
    存储用户之间或社团之间的相似度
    """
    
    MATRIX_TYPE_CHOICES = [
        ('user_user', '用户-用户相似度'),
        ('item_item', '物品-物品相似度'),
        ('user_club', '用户-社团偏好矩阵'),
    ]
    
    matrix_type = models.CharField('矩阵类型', max_length=20, choices=MATRIX_TYPE_CHOICES)
    
    # 关联ID（可以是用户ID或社团ID）
    entity_a = models.IntegerField('实体A ID')
    entity_b = models.IntegerField('实体B ID')
    
    # 相似度/偏好值
    similarity = models.FloatField('相似度', help_text='-1到1或0到1')
    
    # 元数据
    algorithm = models.CharField('算法', max_length=50, default='cosine')
    sample_size = models.IntegerField('样本数', default=0, 
                                       help_text='计算时使用的样本数量')
    
    computed_at = models.DateTimeField('计算时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'similarity_matrix'
        verbose_name = '相似度矩阵'
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['matrix_type', 'entity_a', 'entity_b']),
            models.Index(fields=['matrix_type', '-similarity']),
        ]
    
    def __str__(self):
        return f"{self.matrix_type}: {self.entity_a} <-> {self.entity_b} = {self.similarity:.4f}"


class RecommendationFeedback(models.Model):
    """
    推荐反馈表
    收集用户对推荐结果的反馈
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendation_feedback')
    club_id = models.IntegerField('社团ID')
    
    # 反馈类型
    feedback_type = models.CharField('反馈类型', max_length=20,
                                     choices=[
                                         ('click', '点击查看'),
                                         ('like', '感兴趣'),
                                         ('dislike', '不感兴趣'),
                                         ('apply', '申请加入'),
                                         ('ignore', '忽略'),
                                     ])
    
    # 推荐时的分数
    original_score = models.FloatField('推荐分数', default=0)
    
    # 额外反馈
    reason = models.TextField('原因', blank=True, 
                               help_text='用户选择不感兴趣的原因')
    
    created_at = models.DateTimeField('反馈时间', auto_now_add=True)
    
    class Meta:
        db_table = 'recommendation_feedback'
        verbose_name = '推荐反馈'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - Club {self.club_id} - {self.feedback_type}"


class ClubRecommendationData(models.Model):
    """
    社团推荐扩展数据
    存储社团的推荐相关扩展数据
    与主Club模型通过club_id关联
    """
    
    club = models.OneToOneField('clubs.Club', on_delete=models.CASCADE, primary_key=True, related_name='recommendation_data')
    
    # 社团活跃时间段（JSON格式）
    active_time = models.JSONField('主要活动时间段', default=dict, blank=True)
    
    # 推荐相关统计
    view_count = models.IntegerField('浏览次数', default=0)
    like_count = models.IntegerField('收藏次数', default=0)
    apply_count = models.IntegerField('申请次数', default=0)
    recommendation_score = models.FloatField('推荐指数', default=0)
    
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        db_table = 'club_recommendation_data'
        verbose_name = '社团推荐数据'
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return f"Recommendation data for {self.club.name}"
