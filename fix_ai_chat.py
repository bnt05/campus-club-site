#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复MBTI测试：更新ai_chat函数使用Session存储对话历史
"""
import os
import sys

filepath = r'D:\campus_club_site\clubs\ai_views.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 旧的ai_chat函数
old_chat_func = '''@csrf_exempt
@require_http_methods(["POST"])
def ai_chat(request):
    """AI聊天接口"""
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        conversation_history = data.get('history', [])
        
        if not user_message:
            return JsonResponse({'error': '消息不能为空'}, status=400)
        
        reply = chat(request.user, user_message, conversation_history)
        
        return JsonResponse({'reply': reply})
    
    except json.JSONDecodeError:
        return JsonResponse({'error': '无效的JSON格式'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)'''

# 新的ai_chat函数 - 使用Session存储对话历史
new_chat_func = '''@csrf_exempt
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

if old_chat_func in content:
    new_content = content.replace(old_chat_func, new_chat_func)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('SUCCESS: ai_chat function updated to use Session')
else:
    print('ERROR: could not find old ai_chat function')
    print('Looking for:')
    print(old_chat_func[:300])
