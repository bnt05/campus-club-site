#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
修复MBTI测试功能：更新SYSTEM_PROMPT和ai_chat函数使用Session
"""
import os
import sys

filepath = r'D:\campus_club_site\clubs\ai_service.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 新的SYSTEM_PROMPT - 包含完整的8题MBTI题库和严格规则
new_system_prompt = '''【角色】
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
第8题：你更习惯？[A] 固定日程安排 [B] 随机灵活安排'''

# 查找并替换get_system_prompt函数
old_func_start = content.find('def get_system_prompt(')
old_func_end = content.find('\ndef get_data_context(')

if old_func_start == -1 or old_func_end == -1:
    print('ERROR: Could not find get_system_prompt function')
    sys.exit(1)

new_function = f'''def get_system_prompt(user=None):
    """生成极简版系统提示词，严格限制回复格式"""
    return """{new_system_prompt}"""


'''

new_content = content[:old_func_start] + new_function + content[old_func_end:]

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('SUCCESS: get_system_prompt updated with complete MBTI rules')
