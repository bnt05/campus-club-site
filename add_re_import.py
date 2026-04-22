#!/usr/bin/env python
# -*- coding: utf-8 -*-
filepath = r'D:\campus_club_site\clubs\ai_views.py'
with open(filepath, 'rb') as f:
    content = f.read()

# 查找 import json 的位置并在其后添加 import re
old = b'import json\r\n'
new = b'import json\r\nimport re\r\n'

if old in content:
    content = content.replace(old, new)
    with open(filepath, 'wb') as f:
        f.write(content)
    print('SUCCESS: Added import re')
else:
    print('ERROR: Could not find import json line')
