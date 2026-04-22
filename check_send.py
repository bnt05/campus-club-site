#!/usr/bin/env python
# -*- coding: utf-8 -*-
with open('clubs/templates/clubs/ai_floating_widget.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找 sendQuickMessage 函数
import re
# 找到函数定义
match = re.search(r'function sendQuickMessage\([^\)]*\)\s*\{([^}]+)\}', content, re.DOTALL)
if match:
    print('sendQuickMessage function body:')
    print(match.group(1)[:500])
else:
    print('sendQuickMessage function not found')
    
# 查找 fetch 调用上下文
match2 = re.search(r'fetch\([^)]+\)[^{]*\{[^}]*\}', content, re.DOTALL)
if match2:
    print('\nfetch call:')
    print(match2.group(0)[:500])
