#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

with open('clubs/urls.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 查找所有 path(...) 
paths = re.findall(r"path\(['\"](.*?)['\"],\s*\w+", content)
for p in paths:
    print(p)
