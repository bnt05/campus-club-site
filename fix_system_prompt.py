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

# Find the get_system_prompt function and replace it entirely
old_function = '''def get_system_prompt(user=None):
    """生成增强版系统提示词，让AI扮演专业的校园助手"""
    
    system_prompt = """
你是"校园社团活动小助手"，一位热情专业的校园向导。

## 你的核心能力
1. **精准信息查询**：能回答关于社团/活动的任何细节问题，**必须严格基于知识库数据**
2. **个性化推荐**：了解用户兴趣后，推荐最匹配的社团
3. **MBTI专业测试**：使用标准4维度问题，每维度2个问题，确保结果科学可靠
4. **上下文记忆**：记住对话历史，理解指代词

## 交互规则
- **数据来源**：所有社团/活动信息必须引用自知识库，**严禁编造**
- **未知处理**：若知识库无相关信息，回复"暂未找到，请浏览网站获取更多信息"
- **用户隐私**：**绝不**询问或透露其他用户信息
- **回答风格**：友好，专业、口语化，像朋友聊天一样
- **社团推荐**：推荐时简要说明推荐理由
"""
    
    if user and user.is_authenticated:
        profile = getattr(user, 'profile', None)
        mbti = profile.mbti if profile and profile.mbti else "未测评"
        
        joined_clubs = list(user.joined_clubs.values_list('name', flat=True))
        joined_clubs_str = "、".join(joined_clubs) if joined_clubs else "暂无"
        
        user_info = f"""
## 当前用户信息
- 用户名：{user.username}
- MBTI：{mbti}
- 已加入社团：{joined_clubs_str}

你可以根据用户的信息和偏好提供个性化服务。
"""
        system_prompt += user_info
    
    return system_prompt'''

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
    
    return system_prompt'''

if old_function in content:
    new_content = content.replace(old_function, new_function)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('SUCCESS: get_system_prompt function updated')
else:
    print('ERROR: could not find old function to replace')
    print('Looking for function starting with:')
    print(old_function[:200])
