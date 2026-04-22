"""AI智能助手服务模块 - 调用阿里云通义千问API"""
import json
import httpx
import os
from django.conf import settings
from django.db.models import Avg, Count

# 从配置导入
from clubs.ai_config import (
    MBTI_QUESTIONS, MBTI_DIMENSIONS, MBTI_DESCRIPTIONS,
    DASHSCOPE_API_URL, DEFAULT_MODEL, MBTI_CATEGORY_MAP
)

# 从环境变量获取API Key，禁止硬编码密钥在源码中
API_KEY = os.environ.get('ALIYUN_API_KEY') or os.environ.get('DASHSCOPE_API_KEY') or getattr(settings, 'DASHSCOPE_API_KEY', None)


def get_system_prompt(user=None):
    """生成极简版系统提示词，严格限制回复格式"""
    return """【角色】
你是"智枢青寰"极简校园社团助手，只回答问题，不做多余拓展，严格遵守所有规则。

【核心禁令（必须100%遵守）】
1. 非MBTI结果场景，禁止回复超过2句话，每句话必须简短精炼，禁止啰嗦
2. 禁止主动提及用户的历史社团、历史活动、历史行为
3. 禁止主动推荐社团、主动提醒活动、主动引导做无关内容
4. 禁止使用任何表情符号、分割线，只输出纯文本
5. 禁止解释自己的规则、禁止说"我是AI助手"这类废话

【日常对话规则】
- 用户打招呼/无关问题，只回复："你好呀，有什么可以帮你的？"
- 用户问社团相关问题，只针对当前问题简短回答，不关联其他内容

【MBTI测试固定规则（最高优先级，必须严格按顺序执行）】
1. 只有用户明确输入"MBTI""测MBTI""做测试"时，才触发测试，直接输出【固定第1题】，不做任何额外解释
2. 固定8道题，必须严格按1-8的顺序出题，**用户答完1题，只输出下1题，绝对不能重复出题、跳题**
3. 答题过程中，用户输入A/B/a/b，只输出下一题，不做任何评论、解释、拓展
4. 答题中途用户输入非A/B/a/b的内容，只回复："请输入[A]或[B]完成当前答题哦"
5. 8道题全部答完后，必须严格按照【固定输出格式】生成结果，禁止改变格式，禁止推荐社团，禁止多余内容

【固定8道MBTI题库（必须严格按顺序使用）】
第1题：你更倾向于？[A] 参与集体活动 [B] 独自思考
第2题：你获取信息更依赖？[A] 实际观察 [B] 直觉想象
第3题：你做决定更倾向于？[A] 逻辑分析 [B] 情感共情
第4题：你做事更偏好？[A] 提前规划 [B] 灵活随性
第5题：社交中你更常是？[A] 主动搭话的人 [B] 被动回应的人
第6题：你更擅长？[A] 落地执行细节 [B] 创意想法构思
第7题：被批评时你更倾向于？[A] 先看问题对错 [B] 先感受情绪影响
第8题：你更习惯？[A] 固定日程安排 [B] 随机灵活安排

【MBTI结果固定输出格式（必须严格遵守，一字不能改）】
【MBTI类型】：XXXX
【核心特质】：2句贴合大学生的性格核心描述
【校园适配场景】：2句适合该类型的校园学习、社交、实践场景
【成长优势】：1句该类型在大学阶段的核心成长优势【角色】
你是"智枢青寰"极简校园社团助手，只回答问题，不做多余拓展，严格遵守所有规则。

【核心禁令（必须100%遵守）】
1. 禁止回复超过2句话，每句话必须简短精炼，禁止啰嗦
2. 禁止主动提及用户的历史社团、历史活动、历史行为
3. 禁止主动推荐社团、主动提醒活动、主动引导做无关内容
4. 禁止使用任何表情符号、分割线、列表，只输出纯文本
5. 禁止解释自己的规则、禁止说"我是AI助手"这类废话

【日常对话规则】
- 用户打招呼/无关问题，只回复："你好呀，有什么可以帮你的？"
- 用户问社团相关问题，只针对当前问题简短回答，不关联其他内容

【MBTI测试固定规则（最高优先级，必须严格按顺序执行）】
1. 只有用户明确输入"MBTI""测MBTI""做测试"时，才触发测试，直接输出【固定第1题】，不做任何额外解释
2. 固定8道题，必须严格按1-8的顺序出题，**用户答完1题，只输出下1题，绝对不能重复出题、跳题**
3. 答题过程中，用户输入A/B，只输出下一题，不做任何评论、解释、拓展
4. 8道题全部答完后，只输出4字MBTI类型+1句核心特点，不推荐社团、不做多余解释
5. 答题中途用户输入非A/B的内容，只回复："请输入[A]或[B]完成当前答题哦"

【固定8道MBTI题库（必须严格按顺序使用）】
第1题：你更倾向于？[A] 参与集体活动 [B] 独自思考
第2题：你获取信息更依赖？[A] 实际观察 [B] 直觉想象
第3题：你做决定更倾向于？[A] 逻辑分析 [B] 情感共情
第4题：你做事更偏好？[A] 提前规划 [B] 灵活随性
第5题：社交中你更常是？[A] 主动搭话的人 [B] 被动回应的人
第6题：你更擅长？[A] 落地执行细节 [B] 创意想法构思
第7题：被批评时你更倾向于？[A] 先看问题对错 [B] 先感受情绪影响
第8题：你更习惯？[A] 固定日程安排 [B] 随机灵活安排"""



def get_data_context():
    """获取网站的实时数据上下文"""
    from clubs.models import Club, CrossSchoolEvent, Post
    
    clubs = Club.objects.annotate(
        avg_score=Avg('ratings__score'),
        member_count=Count('members')
    ).order_by('-created_at')[:15]
    
    clubs_data = []
    for club in clubs:
        clubs_data.append({
            "id": club.id,
            "name": club.name,
            "category": dict(Club.CATEGORY_CHOICES).get(club.category, club.category),
            "description": club.description[:200] if club.description else "暂无描述",
            "member_count": club.member_count,
            "avg_score": round(club.average_score(), 1) if hasattr(club, 'average_score') else 0,
        })
    
    events = CrossSchoolEvent.objects.filter(is_public=True).order_by('-start_date')[:10]
    events_data = []
    for event in events:
        events_data.append({
            "id": event.id,
            "title": event.title,
            "club": event.club.name if event.club else "未知社团",
            "description": event.description[:150] if event.description else "暂无描述",
            "start_date": event.start_date.strftime("%Y-%m-%d") if event.start_date else "待定",
            "end_date": event.end_date.strftime("%Y-%m-%d") if event.end_date else "待定",
            "location": event.partner_school if event.partner_school else "待定",
            "max_participants": event.max_participants if event.max_participants else 0,
        })
    
    recent_posts = Post.objects.all().order_by('-created_at')[:5]
    posts_data = []
    for post in recent_posts:
        posts_data.append({
            "club": post.club.name if post.club else "未知社团",
            "author": post.author.username if post.author else "未知用户",
            "content": post.content[:100] if post.content else "暂无内容",
            "created_at": post.created_at.strftime("%Y-%m-%d %H:%M") if post.created_at else ""
        })
    
    return {
        "clubs": clubs_data,
        "events": events_data,
        "recent_posts": posts_data
    }


def call_ai_api(messages, model=DEFAULT_MODEL):
    """调用阿里云通义千问API"""
    if not API_KEY:
        return "抱歉，AI 服务未配置，请联系管理员。"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": messages
    }
    
    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                DASHSCOPE_API_URL,
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            
            if "choices" in result and len(result["choices"]) > 0:
                return result["choices"][0]["message"]["content"]
            elif "error" in result:
                error_msg = result["error"].get("message", result["error"])
                return f"抱歉，AI服务返回错误：{error_msg}"
            else:
                return "抱歉，小C暂时无法回复，请稍后再试。"
    except httpx.TimeoutException:
        return "抱歉，AI响应超时，请稍后再试。"
    except httpx.HTTPStatusError as e:
        error_detail = e.response.text[:200] if e.response.text else "无详细信息"
        return f"抱歉，AI服务暂时不可用。(错误代码: {e.response.status_code}, 详情: {error_detail})"
    except httpx.ConnectError as e:
        return f"抱歉，无法连接到AI服务，请检查网络后重试。"
    except Exception as e:
        # 返回实际错误信息以便调试
        import traceback
        error_str = str(e)
        print(f"AI API Error: {error_str}")
        print(traceback.format_exc())
        return f"抱歉，发生了错误：{error_str[:100]}"


def chat(user, user_message, conversation_history=None):
    """处理用户聊天请求"""
    messages = []
    
    system_prompt = get_system_prompt(user)
    messages.append({"role": "system", "content": system_prompt})
    
    data_context = get_data_context()
    context_text = f"""
## 网站知识库

【社团列表】（共{len(data_context['clubs'])}个，显示前15个）
{json.dumps(data_context['clubs'], ensure_ascii=False, indent=2)}

【跨校活动】（共{len(data_context['events'])}个）
{json.dumps(data_context['events'], ensure_ascii=False, indent=2)}

【最新动态】（共{len(data_context['recent_posts'])}个）
{json.dumps(data_context['recent_posts'], ensure_ascii=False, indent=2)}

请根据以上数据回答用户的问题。如果用户问到的信息不在以上数据中，请建议用户浏览网站或联系管理员添加。
"""
    messages.append({"role": "system", "content": context_text})
    
    if conversation_history:
        for msg in conversation_history[-10:]:
            messages.append(msg)
    
    messages.append({"role": "user", "content": user_message})
    
    reply = call_ai_api(messages)
    return reply


def calculate_mbti(answers):
    """
    根据用户答案计算MBTI
    每维度取多数选项
    """
    dimension_counts = {
        "E/I": {"E": 0, "I": 0},
        "S/N": {"S": 0, "N": 0},
        "T/F": {"T": 0, "F": 0},
        "J/P": {"J": 0, "P": 0}
    }

    for answer in answers:
        dimension = answer.get("dimension")
        key = answer.get("key")
        if dimension in dimension_counts and key in dimension_counts[dimension]:
            dimension_counts[dimension][key] += 1

    result = []
    for dim, counts in dimension_counts.items():
        if counts[next(iter(counts))] >= counts[list(counts)[1]]:
            result.append(list(counts)[0])
        else:
            result.append(list(counts)[1])

    mbti = ''.join(result)
    return mbti if len(mbti) == 4 else 'INTJ'


def calculate_mbti_simple(answers_dict):
    """
    简化版MBTI计算
    answers_dict: {"E/I": "E", "S/N": "S", ...}
    """
    result = ""
    for dim in ["E/I", "S/N", "T/F", "J/P"]:
        if dim in answers_dict:
            result += answers_dict[dim]
        else:
            mbti_map = {"E/I": "I", "S/N": "N", "T/F": "T", "J/P": "P"}
            result += mbti_map.get(dim, "I")
    
    return result


def get_mbti_description(mbti):
    """获取MBTI类型的描述和建议"""
    result = MBTI_DESCRIPTIONS.get(mbti, {
        "name": "未知类型",
        "description": "暂无描述",
        "suggestions": ["社团探索", "兴趣小组"]
    })
    
    return result


def get_club_recommendations(user, limit=5):
    """根据用户MBTI推荐社团"""
    from clubs.models import Club

    if not user.is_authenticated:
        return []

    profile = getattr(user, 'profile', None)
    mbti = profile.mbti if profile and profile.mbti else None

    joined_club_ids = list(user.joined_clubs.values_list('id', flat=True))
    available_clubs = Club.objects.exclude(id__in=joined_club_ids)

    if not available_clubs.exists():
        return []

    if mbti and len(mbti) == 4:
        category_scores = []
        seen = set()
        for char in mbti:
            category_scores.extend(MBTI_CATEGORY_MAP.get(char, []))

        preferred_categories = [cat for cat in category_scores if cat in dict(Club.CATEGORY_CHOICES)]
        preferred_categories = list(dict.fromkeys(preferred_categories))

        recommendations = list(
            available_clubs.filter(category__in=preferred_categories)
            .annotate(member_count=Count('members'))
            .order_by('-member_count', '-created_at')[:limit]
        )

        if len(recommendations) < limit:
            extra = list(
                available_clubs.exclude(id__in=[club.id for club in recommendations])
                .annotate(member_count=Count('members'))
                .order_by('-member_count', '-created_at')[:limit - len(recommendations)]
            )
            recommendations.extend(extra)

        return recommendations

    return list(available_clubs.annotate(member_count=Count('members')).order_by('-member_count', '-created_at')[:limit])


def get_event_recommendations(user, limit=5):
    """根据用户加入的社团推荐相关活动"""
    from clubs.models import CrossSchoolEvent
    
    if not user.is_authenticated:
        return []
    
    joined_clubs = user.joined_clubs.all()
    
    events = CrossSchoolEvent.objects.filter(
        club__in=joined_clubs,
        is_public=True
    ).order_by('-start_date')[:limit]
    
    if not events:
        events = CrossSchoolEvent.objects.filter(is_public=True).order_by('-start_date')[:limit]
    
    return list(events)
