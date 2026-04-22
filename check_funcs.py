#!/usr/bin/env python
# -*- coding: utf-8 -*-
with open('clubs/templates/clubs/ai_floating_widget.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找 getCookie 函数
if 'function getCookie' in content:
    print('getCookie function found')
elif 'getCookie(' in content:
    print('getCookie is used but function not defined')
else:
    print('getCookie not found')

# 查找 sendAiMessage 函数
if 'function sendAiMessage' in content:
    print('sendAiMessage function found')
elif 'sendAiMessage' in content:
    print('sendAiMessage is used')
    
# 查找 aiConversationHistory
if 'aiConversationHistory' in content:
    print('aiConversationHistory found')
