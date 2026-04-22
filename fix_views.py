import os
import sys

# Fix views.py encoding issues
views_path = r'D:\campus_club_site\clubs\views.py'

with open(views_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix corrupted strings (replace template path)
content = content.replace('clubs/cross_school_event_form.html', 'clubs/event_create.html')

# Fix garbled Chinese characters (common patterns)
content = content.replace('�?', '。')
content = content.replace('已登录�?', '已登录。')
content = content.replace('社团创建成功�?', '社团创建成功。')
content = content.replace('编辑简介�?', '编辑简介。')
content = content.replace('简介已更新�?', '简介已更新。')
content = content.replace('发布活动社团�?', '发布活动社团。')
content = content.replace('选择发布活动�?', '选择发布活动。')
content = content.replace('为自己创建�?', '为自己创建。')
content = content.replace('活动创建成功�?', '活动创建成功。')
content = content.replace('活动编辑成功�?', '活动编辑成功。')
content = content.replace('活动删除成功�?', '活动删除成功。')

with open(views_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed views.py')
