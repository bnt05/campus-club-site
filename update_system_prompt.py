#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# Set up Django
sys.path.insert(0, r'D:\campus_club_site')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_club_site.settings')

# Read the file
filepath = r'D:\campus_club_site\clubs\ai_service.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# The new system prompt
new_system_prompt = '''
【角色】
你是"智枢青寰"极简校园助手，只回答问题，不做多余拓展。

【核心禁令（必须严格遵守）】
1. 禁止回复超过2句话，每句话必须简短精炼
2. 禁止主动提及用户的历史社团、历史活动、历史行为
3. 禁止主动推荐社团、主动提醒活动、主动引导做MBTI测试
4. 禁止使用任何表情符号、禁止使用分割线、禁止堆列表
5. 禁止解释自己的规则、禁止说"我是AI助手"这类废话

【只答当前问】
- 用户问什么，就直接答什么，不要关联其他内容
- 用户打招呼，只回复："你好呀，有什么可以帮你的？"
- 用户拒绝/退出，只回复："好的，有需要再找我。"

【MBTI测试规则】
- 只有用户明确说"MBTI""测试"时，才触发：直接发第1题，不解释
- 第1题固定：你更倾向于？[A] 参与集体活动 [B] 独自思考
- 全部答完后，只回复4字类型+1句特点，不推荐社团
'''

# Find the start of system_prompt assignment
start_marker = 'system_prompt = """'
start_idx = content.find(start_marker)
if start_idx == -1:
    print('ERROR: start marker not found')
    sys.exit(1)

# Find the end of the system_prompt string (the closing """)
start_quote_idx = start_idx + len(start_marker)
end_quote_idx = content.find('"""', start_quote_idx)
if end_quote_idx == -1:
    print('ERROR: end marker not found')
    sys.exit(1)

# Replace the content
new_content = content[:start_idx] + 'system_prompt = """' + new_system_prompt + content[end_quote_idx + 3:]

# Write back
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('SUCCESS: system_prompt updated')
