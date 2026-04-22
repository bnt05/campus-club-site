#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

filepath = r'D:\campus_club_site\clubs\ai_views.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 新的ai_chat函数 - 包含MBTI结果提取和保存功能
new_ai_chat = '''@csrf_exempt
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
                reply = f"{reply}\n\n✅ 你的MBTI类型【{mbti_type}】已保存到用户中心！"
            except Exception as profile_error:
                print(f"保存MBTI失败: {profile_error}")
        
        elif mbti_match and not request.user.is_authenticated:
            # 用户未登录
            mbti_type = mbti_match.group(1)
            reply = f"{reply}\n\n⚠️ 请登录后可将MBTI结果【{mbti_type}】保存到用户中心！"
        # ========== MBTI保存功能结束 ==========
        
        return JsonResponse({'reply': reply})
    
    except json.JSONDecodeError:
        return JsonResponse({'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)'''

old_ai_chat = '''@csrf_exempt
@require_http_methods(["POST"])
def ai_chat(request):
    """AI聊天接口 - 使用Session存储对话历史"""
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
        
        return JsonResponse({'reply': reply})
    
    except json.JSONDecodeError:
        return JsonResponse({'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)'''

if old_ai_chat in content:
    content = content.replace(old_ai_chat, new_ai_chat)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('SUCCESS: ai_chat function updated with MBTI extraction and save')
else:
    print('ERROR: could not find old ai_chat function')
    print('Looking for pattern...')
