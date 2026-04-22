# Fix corrupted strings in views.py
with open(r'D:\campus_club_site\clubs\views.py', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Replace corrupted strings
replacements = {
    'ä»¬ç¤¾åº�å': '只有社团成员可以发布动态',
    'ä»¬ç¤¾åº�å'ä»¬å'ä»¥å'å¸ƒåŠ¨æ€å': '只有社团成员可以发布动态',
    'åŠ¨æ€å·²å'å¸ƒã€': '动态已发布',
    'åŠ¨æ€å·²å'å¸ƒ': '动态已发布',
    'ä»¬ç¤¾åº�å'ä»¬å'ä»¥å'å¸ƒåŠ¨æ€å': '只有社团成员可以发布动态',
    'ä»¬ç¤¾åº�å'ä»¬å'ä»¥å'å¸ƒåŠ¨æ€å': '只有社团成员可以发布动态',
    'ç¤¾åº�å·²å'å¸ƒ': '社团已发布',
    'ç¤¾æˆ�åŠŸ': '社团成功',
    'ä¿®æ”¹å·²å®Œ': '修改已完成',
    'åŠ¨æ€å·²åˆ é™': '动态已删除',
    'å¯¹è±¡ä¿®æ”¹å·²å®Œ': '对象修改已完成',
    'ç¤¾å'æ´»åŠ¨': '社团活动',
    'ä»¬ç¤¾åº�å'ä»¬å'ä»¥å'å¸ƒåŠ¨æ€å': '只有社团成员可以发布动态',
    'ä»¬ç¤¾åº�å'ä»¬å'ä»¥å'å¸ƒåŠ¨æ€å': '只有社团成员可以发布动态',
    'é»¬è®¤åˆ†ç±»': '默认分类',
    'ä»¬ç¤¾åº�å'ä»¬å'ä»¥å'å¸ƒåŠ¨æ€å': '只有社团成员可以发布动态。',
}

for corrupted, correct in replacements.items():
    content = content.replace(corrupted, correct)

with open(r'D:\campus_club_site\clubs\views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed views.py')
