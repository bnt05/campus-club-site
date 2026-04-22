# -*- coding: utf-8 -*-
"""
社团智能推荐系统 - URL配置
"""

from django.urls import path
from clubs.recommendation_views import (
    RecommendationAPI, StudentProfileAPI, InterestTagsAPI,
    StatisticsAPI, SimilarityComputeAPI, ActivityTimelineAPI,
    BehaviorRecordAPI
)

app_name = 'recommendation'

urlpatterns = [
    # 推荐相关
    path('recommend/', RecommendationAPI.as_view(), name='recommend'),
    path('recommend/refresh/', RecommendationAPI.as_view(), name='recommend_refresh'),
    
    # 学生档案
    path('profile/', StudentProfileAPI.as_view(), name='profile'),
    
    # 兴趣标签
    path('tags/', InterestTagsAPI.as_view(), name='tags'),
    
    # 统计数据
    path('stats/', StatisticsAPI.as_view(), name='stats'),
    path('stats/overview/', StatisticsAPI.as_view(), {'type': 'overview'}, name='stats_overview'),
    path('stats/clubs/', StatisticsAPI.as_view(), {'type': 'clubs'}, name='stats_clubs'),
    path('stats/activities/', StatisticsAPI.as_view(), {'type': 'activities'}, name='stats_activities'),
    path('stats/students/', StatisticsAPI.as_view(), {'type': 'students'}, name='stats_students'),
    path('stats/heatmap/', StatisticsAPI.as_view(), {'type': 'heatmap'}, name='stats_heatmap'),
    path('stats/recommendation/', StatisticsAPI.as_view(), {'type': 'recommendation'}, name='stats_recommendation'),
    
    # 相似度计算
    path('similarity/compute/', SimilarityComputeAPI.as_view(), name='similarity_compute'),
    
    # 活动时间线
    path('timeline/', ActivityTimelineAPI.as_view(), name='timeline'),
    
    # 行为记录
    path('behavior/', BehaviorRecordAPI.as_view(), name='behavior'),
]
