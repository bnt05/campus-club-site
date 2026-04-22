#!/usr/bin/env python
# -*- coding: utf-8 -*-
with open('clubs/templates/clubs/ai_floating_widget.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找 fetch 调用
if 'fetch(' in content:
    print('fetch() found')
    
# 查找 /api/ 路径
import re
api_calls = re.findall(r'/api/[^\s"\'<>]+', content)
print('API calls:', api_calls)

# 查找发送消息的函数
if 'sendQuickMessage' in content:
    print('sendQuickMessage found')
    
# 查找消息内容
if 'user_input' in content:
    print('user_input found in template')
if 'message' in content:
    print('message found in template')
