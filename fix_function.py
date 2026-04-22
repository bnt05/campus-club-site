#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# Read the file
filepath = r'D:\campus_club_site\clubs\ai_service.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the get_system_prompt function - it starts with "def get_system_prompt" and ends before "def get_data_context"
func_start = content.find('def get_system_prompt(')
func_end = content.find('\ndef get_data_context(')

if func_start == -1 or func_end == -1:
    print('ERROR: Could not find function boundaries')
    sys.exit(1)

print(f'Found function from position {func_start} to {func_end}')

# The new function
new_function = '''def get_system_prompt(user=None):
    """生成极简版系统提示词，严格限制回复格式"""
    
    system_prompt = """
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
"""
    
    return system_prompt

'''

# Replace the old function with the new one
new_content = content[:func_start] + new_function + content[func_end:]

# Write back
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('SUCCESS: Function replaced')
