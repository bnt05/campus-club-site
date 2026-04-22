#!/usr/bin/env python
# -*- coding: utf-8 -*-
with open('clubs/templates/clubs/ai_floating_widget.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 检查关键内容
checks = [
    ('ai-quick-features', '快速功能区域'),
    ('sendQuickMessage', '发送消息函数'),
    ('一键MBTI', '一键MBTI按钮'),
    ('getCookie', 'getCookie函数'),
]

for keyword, label in checks:
    if keyword in content:
        print(f'[OK] {label}')
    else:
        print(f'[MISSING] {label}')
