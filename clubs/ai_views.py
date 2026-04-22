"""
AI智能助手API视图
"""
import json
import re
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count

from clubs.models import Club, CrossSchoolEvent, Post
from clubs.ai_service import (
    chat, calculate_mbti, calculate_mbti_simple, get_mbti_description,
    get_club_recommendations, get_event_recommendations
)
from clubs.ai_config import MBTI_QUESTIONS, MBTI_DESCRIPTIONS


@csrf_exempt
@require_http_methods(["POST"])
def ai_chat(request):
    """AI聊天接口 - 使用Session存储对话历史，提取并保存MBTI结果"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        if not user_message:
            return JsonResponse({'error': '消息不能为空'}, status=400)
        
        # 从Session获取对话历史，如果不存在则初始化为空列表
        chat_history = request.session.get('chat_history', [])
        
        # 调用chat函数，传入对话历史
        reply = chat(request.user, user_message, chat_history)
        
        # 将用户消息和AI回复都加入到对话历史
        chat_history.append({"role": "user", "content": user_message})
        chat_history.append({"role": "assistant", "content": reply})
        
        # 保存更新后的对话历史到Session（保留最近20条）
        chat_history = chat_history[-20:]
        request.session['chat_history'] = chat_history
        request.session.set_expiry(7200)  # 2小时有效期
        
        # ========== 核心新增：自动识别MBTI结果，上传用户中心 ==========
        # MBTI类型提取正则（匹配4位大写字母）
        mbti_regex = re.compile(r"【MBTI类型】：([ISTJISTPISFJISFPINFJINFPINTJINTPESFPESTJESFPENFJENTPENFPENTJ]{4})")
        mbti_match = mbti_regex.search(reply)
        
        if mbti_match and request.user.is_authenticated:
            # 用户已登录，保存MBTI到Profile
            mbti_type = mbti_match.group(1)
            try:
                profile = request.user.profile
                profile.mbti_type = mbti_type
                profile.save()
                reply = reply + "\n\n✅ 你的MBTI类型【" + mbti_type + "】已保存到用户中心！"
            except Exception as profile_error:
                print(f"保存MBTI失败: {profile_error}")
        
        elif mbti_match and not request.user.is_authenticated:
            # 用户未登录
            mbti_type = mbti_match.group(1)
            reply = reply + "\n\n⚠️ 请登录后可将MBTI结果【" + mbti_type + "】保存到用户中心！"
        # ========== MBTI保存功能结束 ==========
        
        return JsonResponse({'reply': reply})
    
    except json.JSONDecodeError:
        return JsonResponse({'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def mbti_questions(request):
    """获取MBTI测试问题（8题）"""
    return JsonResponse({
        'questions': MBTI_QUESTIONS,
        'total': len(MBTI_QUESTIONS)
    })


@login_required
@require_http_methods(["POST"])
def mbti_submit(request):
    """
    提交MBTI测试答案并计算结果
    新版格式：{"answers": [{"dimension": "E/I", "key": "E"}, ...]}
    兼容旧格式：{"answers": {"E/I": "E", "S/N": "S", ...}}
    """
    try:
        data = json.loads(request.body)
        answers = data.get('answers', {})
        
        if not answers:
            return JsonResponse({'error': '答案不能为空'}, status=400)
        
        # 兼容新旧格式
        if isinstance(answers, list):
            # 新格式：[{"dimension": "E/I", "key": "E"}, ...]
            mbti = calculate_mbti(answers)
        else:
            # 旧格式：{"E/I": "E", "S/N": "S", ...}
            mbti = calculate_mbti_simple(answers)
        
        # 验证MBTI有效性
        valid_mbti_types = list(MBTI_DESCRIPTIONS.keys())
        if mbti not in valid_mbti_types:
            return JsonResponse({'error': '无效的 MBTI 类型'}, status=400)
        
        description = get_mbti_description(mbti)
        
        # 保存到用户资料
        profile = request.user.profile
        profile.mbti_type = mbti
        profile.save()
        
        # 获取推荐社团
        recommendations = get_club_recommendations(request.user, limit=3)
        recommended_clubs = [{
            'name': club.name,
            'category': dict(Club.CATEGORY_CHOICES).get(club.category, club.category)
        } for club in recommendations]
        
        return JsonResponse({
            'mbti': mbti,
            'name': description['name'],
            'description': description['description'],
            'suggestions': description.get('suggestions', []),
            'recommended_clubs': recommended_clubs
        })
    
    except json.JSONDecodeError:
        return JsonResponse({'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_http_methods(["GET"])
def user_profile_api(request):
    """获取当前用户资料"""
    profile = request.user.profile
    return JsonResponse({
        'username': request.user.username,
        'email': request.user.email,
        'mbti': profile.mbti,
        'mbti_type': profile.mbti_type,
        'joined_clubs': list(request.user.joined_clubs.values('id', 'name'))
    })


@csrf_exempt
@require_http_methods(["POST"])
def api_assistant(request):
    """智能助手代理接口"""
    return ai_chat(request)


@login_required
@require_http_methods(["GET"])
@cache_page(60 * 5)
def api_clubs(request):
    """获取所有社团信息的标准化接口"""
    clubs = Club.objects.annotate(
        avg_score=Avg('ratings__score'),
        member_count=Count('members')
    ).all()
    data = [
        {
            'id': club.id,
            'name': club.name,
            'category': club.category,
            'category_display': dict(Club.CATEGORY_CHOICES).get(club.category, club.category),
            'description': club.description,
            'member_count': club.member_count,
            'avg_score': round(club.average_score(), 1),
            'poster': club.poster.url if club.poster else None,
            'created_at': club.created_at.strftime('%Y-%m-%d')
        }
        for club in clubs
    ]
    return JsonResponse({'clubs': data})


@login_required
@require_http_methods(["GET"])
@cache_page(60 * 5)
def api_events(request):
    """获取近期活动日历的标准化接口"""
    events = CrossSchoolEvent.objects.filter(is_public=True).order_by('-start_date')
    data = [
        {
            'id': event.id,
            'title': event.title,
            'club_id': event.club.id,
            'club': event.club.name,
            'description': event.description,
            'poster': event.poster.url if event.poster else None,
            'start_date': event.start_date.strftime('%Y-%m-%d'),
            'end_date': event.end_date.strftime('%Y-%m-%d'),
            'location': event.partner_school
        }
        for event in events
    ]
    return JsonResponse({'events': data})


@login_required
@require_http_methods(["POST"])
def api_user_mbti(request):
    """用户提交 MBTI 测试结果"""
    return mbti_submit(request)


@login_required
@require_http_methods(["GET"])
def api_user_profile(request):
    """获取当前用户资料（RESTful 版本）"""
    return user_profile_api(request)


@require_http_methods(["GET"])
@cache_page(60 * 5)
def site_data(request):
    """获取网站数据（用于AI助手和前端展示）"""
    clubs = Club.objects.annotate(
        avg_score=Avg('ratings__score'),
        member_count=Count('members')
    ).all()[:20]
    
    clubs_data = []
    for club in clubs:
        clubs_data.append({
            'id': club.id,
            'name': club.name,
            'category': club.category,
            'category_display': dict(Club.CATEGORY_CHOICES).get(club.category, club.category),
            'description': club.description,
            'member_count': club.member_count,
            'avg_score': round(club.average_score(), 1),
            'poster': club.poster.url if club.poster else None,
            'created_at': club.created_at.strftime('%Y-%m-%d')
        })
    
    events = CrossSchoolEvent.objects.filter(is_public=True).order_by('-start_date')[:20]
    events_data = []
    for event in events:
        events_data.append({
            'id': event.id,
            'title': event.title,
            'club': event.club.name,
            'club_id': event.club.id,
            'description': event.description,
            'start_date': event.start_date.strftime('%Y-%m-%d'),
            'end_date': event.end_date.strftime('%Y-%m-%d'),
            'poster': event.poster.url if event.poster else None
        })
    
    categories = [{'value': k, 'label': v} for k, v in Club.CATEGORY_CHOICES]
    
    return JsonResponse({
        'clubs': clubs_data,
        'events': events_data,
        'categories': categories
    })


@login_required
@require_http_methods(["GET"])
def recommendations(request):
    """获取个性化推荐"""
    recommended_clubs = get_club_recommendations(request.user, limit=6)
    recommended_events = get_event_recommendations(request.user, limit=6)
    
    clubs_data = [{
        'id': club.id,
        'name': club.name,
        'category': dict(Club.CATEGORY_CHOICES).get(club.category, club.category),
        'description': club.description[:100],
        'member_count': club.member_count(),
        'avg_score': club.average_score()
    } for club in recommended_clubs]
    
    events_data = [{
        'id': event.id,
        'title': event.title,
        'club': event.club.name,
        'start_date': event.start_date.strftime('%Y-%m-%d'),
        'end_date': event.end_date.strftime('%Y-%m-%d')
    } for event in recommended_events]
    
    return JsonResponse({
        'clubs': clubs_data,
        'events': events_data
    })


