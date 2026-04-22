"""
智能助手配置
"""
import os
from django.conf import settings

# 阿里云API配置 - 优先从Django settings读取，其次从环境变量
DASHSCOPE_API_KEY = getattr(settings, 'DASHSCOPE_API_KEY', None) or os.environ.get('ALIYUN_API_KEY') or os.environ.get('DASHSCOPE_API_KEY')
DASHSCOPE_API_URL = getattr(settings, 'DASHSCOPE_API_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions')
DEFAULT_MODEL = getattr(settings, 'DASHSCOPE_MODEL', 'qwen-plus')

# MBTI测试问题（8题，每维度2题）
MBTI_QUESTIONS = [
    {
        "dimension": "E/I",
        "question": "在社交场合中，你通常会感到？",
        "options": [
            {"key": "E", "text": "精力充沛，喜欢和人交流，从社交中获得能量"},
            {"key": "I", "text": "需要独处来恢复能量，社交后会感到疲惫"}
        ]
    },
    {
        "dimension": "E/I",
        "question": "当你独自一人时，你通常会？",
        "options": [
            {"key": "E", "text": "想念朋友，迫不及待想找人聊天"},
            {"key": "I", "text": "享受独处时光，做自己喜欢的事"}
        ]
    },
    {
        "dimension": "S/N",
        "question": "你更喜欢哪种学习方式？",
        "options": [
            {"key": "S", "text": "通过具体例子和实践操作来理解"},
            {"key": "N", "text": "通过抽象概念和理论思考来理解"}
        ]
    },
    {
        "dimension": "S/N",
        "question": "当你阅读一本书时，你更关注？",
        "options": [
            {"key": "S", "text": "具体的情节和事实细节"},
            {"key": "N", "text": "整体的象征意义和深层含义"}
        ]
    },
    {
        "dimension": "T/F",
        "question": "做决定时，你更看重？",
        "options": [
            {"key": "T", "text": "逻辑和客观分析，追求公平"},
            {"key": "F", "text": "对他人的感受和影响，追求和谐"}
        ]
    },
    {
        "dimension": "T/F",
        "question": "当朋友向你倾诉烦恼时，你通常会？",
        "options": [
            {"key": "T", "text": "分析问题，给出解决方案"},
            {"key": "F", "text": "先安慰情绪，表示理解和支持"}
        ]
    },
    {
        "dimension": "J/P",
        "question": "你更倾向于？",
        "options": [
            {"key": "J", "text": "有计划、有条理，提前安排好一切"},
            {"key": "P", "text": "灵活、随遇而安，享受即兴的乐趣"}
        ]
    },
    {
        "dimension": "J/P",
        "question": "旅行时，你更喜欢？",
        "options": [
            {"key": "J", "text": "提前规划好行程，预订好酒店"},
            {"key": "P", "text": "随性而为，看到喜欢的就多停留"}
        ]
    },
]

# MBTI维度名称映射
MBTI_DIMENSIONS = {
    "E/I": {"name": "外向型 vs 内向型", "E": "外向型(E)", "I": "内向型(I)"},
    "S/N": {"name": "感觉型 vs 直觉型", "S": "感觉型(S)", "N": "直觉型(N)"},
    "T/F": {"name": "思考型 vs 情感型", "T": "思考型(T)", "F": "情感型(F)"},
    "J/P": {"name": "判断型 vs 知觉型", "J": "判断型(J)", "P": "知觉型(P)"},
}

# MBTI到社团类别映射，用于推荐匹配
MBTI_CATEGORY_MAP = {
    'E': ['interest', 'public_welfare', 'other'],
    'I': ['academic', 'culture', 'arts'],
    'S': ['sports', 'public_welfare', 'interest'],
    'N': ['arts', 'academic', 'culture'],
    'T': ['academic', 'sports', 'culture'],
    'F': ['public_welfare', 'arts', 'interest'],
    'J': ['academic', 'public_welfare', 'culture'],
    'P': ['interest', 'sports', 'other'],
}

# MBTI类型描述
MBTI_DESCRIPTIONS = {
    "INTJ": {"name": "建筑师", "description": "富有想象力和战略性的思考者，有独特的想法和强大的执行力。", "suggestions": ["学术科创类社团", "辩论队", "编程社"]},
    "INTP": {"name": "逻辑学家", "description": "创新型的发明家，对知识充满渴望，擅长分析抽象概念。", "suggestions": ["学术科创类社团", "数学社", "科幻协会"]},
    "ENTJ": {"name": "指挥官", "description": "大胆、富有想象力的领导者，具有强大的执行力和决策能力。", "suggestions": ["学生会", "创业协会", "演讲辩论社"]},
    "ENTP": {"name": "辩论家", "description": "聪明好奇的思考者，喜欢挑战传统，不喜欢例行公事。", "suggestions": ["辩论队", "模拟联合国", "创新创业社"]},
    "INFJ": {"name": "提倡者", "description": "安静而神秘，有原则有理想，致力于改善他人生活。", "suggestions": ["公益社团", "志愿者协会", "心理健康社"]},
    "INFP": {"name": "调停者", "description": "理想主义的深思者，追求有意义的人际关系和自我表达。", "suggestions": ["文学社", "诗社", "艺术社团"]},
    "ENFJ": {"name": "主人公", "description": "富有魅力和感染力的领导者，热情且乐于助人。", "suggestions": ["学生会", "社团联合会", "志愿服务社"]},
    "ENFP": {"name": "竞选者", "description": "热情洋溢的创意者，思维活跃，热爱自由和可能性。", "suggestions": ["戏剧社", "动漫社", "音乐社"]},
    "ISTJ": {"name": "物流师", "description": "务实且值得信赖，是组织的支柱，重视承诺和责任。", "suggestions": ["社团管理", "财务协会", "校史馆志愿者"]},
    "ISFJ": {"name": "守护者", "description": "温暖而关怀的保护者，勤奋负责，忠诚于重要的人和事。", "suggestions": ["公益社团", "图书馆志愿者", "敬老院服务社"]},
    "ESTJ": {"name": "总经理", "description": "出色的管理者，果断务实，注重效率和结果。", "suggestions": ["学生会", "社团联合会", "职业发展协会"]},
    "ESFJ": {"name": "执政官", "description": "热情而有责任感的照顾者，喜欢帮助他人，是天生的社交者。", "suggestions": ["学生会", "礼仪社团", "校园媒体"]},
    "ISTP": {"name": "鉴赏家", "description": "大胆而实用的实验家，擅长分析事物的工作原理。", "suggestions": ["科技社团", "机械社", "摄影协会"]},
    "ISFP": {"name": "探险家", "description": "灵活有魅力的艺术家型，追求有意义的美学体验。", "suggestions": ["艺术社团", "音乐社", "舞蹈社"]},
    "ESTP": {"name": "企业家", "description": "聪明且精力充沛的思考者，擅长解决实际问题。", "suggestions": ["创业协会", "营销社团", "体育社团"]},
    "ESFP": {"name": "表演者", "description": "自发性的演员和社交者，生活在他们的热情之中。", "suggestions": ["戏剧社", "主持人协会", "音乐舞蹈社团"]},
}
