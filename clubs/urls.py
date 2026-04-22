from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.http import HttpResponseRedirect
from django.urls import path, re_path

from . import views
from . import ai_views
from . import encyclopedia_views
from . import recommendation_views
from . import recommendation_urls

urlpatterns = [
    path('', views.home, name='home'),
    path('clubs/', views.index, name='index'),
    path('clubs/my/', views.my_clubs, name='my_clubs'),
    path('clubs/create/', views.club_create, name='club_create'),
    path('clubs/<int:club_id>/', views.club_detail, name='club_detail'),
    path('clubs/<int:club_id>/edit/', views.club_edit, name='club_edit'),
    path('clubs/<int:club_id>/join/', views.club_join, name='club_join'),
    path('clubs/<int:club_id>/leave/', views.club_leave, name='club_leave'),
    path('clubs/<int:club_id>/member/<int:user_id>/toggle-admin/', views.toggle_admin, name='toggle_admin'),
    path('clubs/<int:club_id>/post/<int:post_id>/like/', views.post_like, name='post_like'),
    path('clubs/<int:club_id>/post/<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('clubs/<int:club_id>/post/<int:post_id>/pin/', views.post_pin, name='post_pin'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', LoginView.as_view(template_name='clubs/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/password_reset/', PasswordResetView.as_view(template_name='clubs/password_reset_form.html'), name='password_reset'),
    path('accounts/password_reset/done/', PasswordResetDoneView.as_view(template_name='clubs/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='clubs/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', PasswordResetCompleteView.as_view(template_name='clubs/password_reset_complete.html'), name='password_reset_complete'),
    path('events/', views.events_list, name='events_list'),
    path('events/my/', views.my_events, name='my_events'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:event_id>/join/', views.event_join, name='event_join'),
    path('events/<int:event_id>/leave/', views.event_leave, name='event_leave'),
    path('events/<int:event_id>/ical/', views.event_ical, name='event_ical'),
    path('events/<int:event_id>/delete/', views.event_delete, name='event_delete'),
    path('profile/', views.profile, name='profile'),
    
    # AI智能助手
    path('ai/', views.ai_assistant, name='ai_assistant'),
    path('ai/mbti/', views.mbti_test, name='mbti_test'),
    path('api/assistant/', ai_views.api_assistant, name='api_assistant'),
    path('api/ai/chat/', ai_views.ai_chat, name='ai_chat'),
    path('api/ai/mbti/questions/', ai_views.mbti_questions, name='mbti_questions'),
    path('api/ai/mbti/submit/', ai_views.mbti_submit, name='mbti_submit'),
    path('api/user/mbti/', ai_views.api_user_mbti, name='api_user_mbti'),
    path('api/user/profile/', ai_views.api_user_profile, name='api_user_profile'),
    path('api/clubs/', ai_views.api_clubs, name='api_clubs'),
    path('api/events/', ai_views.api_events, name='api_events'),
    path('api/ai/site-data/', ai_views.site_data, name='site_data'),
    path('api/ai/user-profile/', ai_views.user_profile_api, name='user_profile_api'),
    path('api/ai/recommendations/', ai_views.recommendations, name='ai_recommendations'),

    # 活动百科
    path('encyclopedia/', encyclopedia_views.encyclopedia_home, name='encyclopedia_home'),
    re_path(r'^encyclopedia/category/(?P<slug>[\w-]+)/$', encyclopedia_views.encyclopedia_category, name='encyclopedia_category'),
    re_path(r'^encyclopedia/article/(?P<slug>[\w-]+)/$', encyclopedia_views.encyclopedia_article, name='encyclopedia_article'),
    path('encyclopedia/search/', encyclopedia_views.encyclopedia_search, name='encyclopedia_search'),

    # 社团智能推荐系统 API
    path('api/recommend/', recommendation_views.RecommendationAPI.as_view(), name='recommend'),
    path('api/recommend/profile/', recommendation_views.StudentProfileAPI.as_view(), name='recommend_profile'),
    path('api/recommend/tags/', recommendation_views.InterestTagsAPI.as_view(), name='recommend_tags'),
    path('api/recommend/stats/', recommendation_views.StatisticsAPI.as_view(), name='recommend_stats'),
    path('api/recommend/stats/overview/', recommendation_views.StatisticsAPI.as_view(), {'type': 'overview'}, name='recommend_stats_overview'),
    path('api/recommend/stats/clubs/', recommendation_views.StatisticsAPI.as_view(), {'type': 'clubs'}, name='recommend_stats_clubs'),
    path('api/recommend/stats/activities/', recommendation_views.StatisticsAPI.as_view(), {'type': 'activities'}, name='recommend_stats_activities'),
    path('api/recommend/stats/students/', recommendation_views.StatisticsAPI.as_view(), {'type': 'students'}, name='recommend_stats_students'),
    path('api/recommend/stats/heatmap/', recommendation_views.StatisticsAPI.as_view(), {'type': 'heatmap'}, name='recommend_stats_heatmap'),
    path('api/recommend/stats/recommendation/', recommendation_views.StatisticsAPI.as_view(), {'type': 'recommendation'}, name='recommend_stats_recommendation'),
    path('api/recommend/similarity/compute/', recommendation_views.SimilarityComputeAPI.as_view(), name='recommend_similarity_compute'),
    path('api/recommend/timeline/', recommendation_views.ActivityTimelineAPI.as_view(), name='recommend_timeline'),
    path('api/recommend/behavior/', recommendation_views.BehaviorRecordAPI.as_view(), name='recommend_behavior'),

    # 社团智能推荐系统页面
    path('recommend/', views.recommendation_page, name='recommendation_page'),
    path('statistics/', views.statistics_dashboard, name='statistics_dashboard'),
]
