# Fix garbled Chinese characters in views.py

# Read the file
with open(r'D:\campus_club_site\clubs\views.py', 'rb') as f:
    raw = f.read()

# Decode with latin-1 to get the bytes as they are
content = raw.decode('latin-1')

# Replace garbled patterns with correct Chinese characters
replacements = {
    'ä»¬': '只',
    'ç¤¾': '社',
    'åº�': '团',
    'å'ä»¬å'ä»¥å'å¸ƒåŠ¨æ€å': '只有社团成员可以发布动态',
    'åŠ¨æ€å·²å'å¸ƒã': '动态已发布',
    'ä»¬ç¤¾åº�å'ä»¬å'ä»¥å'å¸ƒåŠ¨æ€å': '只有社团成员可以发布动态',
    'åŠ¨æ€å·²å'å¸ƒ': '动态已发布',
    'ç¤¾åº�å·²å'å¸ƒ': '社团已发布',
    'ç¤¾æˆ�åŠŸ': '社团成功',
    'ä¿®æ”¹å·²å®Œ': '修改已完成',
    'åŠ¨æ€å·²åˆ é™': '动态已删除',
    'å¯¹è±¡å·²å'å¯¹': '对象已应对',
    'å¯¹è±¡ä¿®æ”¹å·²å®Œ': '对象修改已完成',
    'ç¤¾å'æ´»åŠ¨': '社活动',
    'å'åŠ¨': '活动',
    'åŠ¨æ€': '动态',
    'ç¤¾åº�': '社团',
    'å'ä»¬': '只能',
    'ä»¬å'ä»¥': '可以',
    'å'å¸ƒ': '发布',
    'åŠ¨': '动',
    'æˆ�åŠŸ': '成功',
    'å®Œ': '完',
    'å·²': '已',
    'åˆ ': '删',
    'é™': '除',
    'ä¿®': '修',
    'æ”¹': '改',
    'å¯¹': '对',
    'è±¡': '象',
    'ã€': '。',
    'ã\x81': '，',
    'ã\x82': '、',
    'ã\x83': '！',
    'ã\x84': '？',
    'ã\x85': '；',
    'ã\x86': '：',
    'ã\x87': '（',
    'ã\x88': '）',
    'ã\x89': '【',
    'ã\x8a': '】',
    'ã\x8b': '『',
    'ã\x8c': '』',
    'ã\x8d': '「',
    'ã\x8e': '」',
    'ã\x8f': '〈',
    'ã\x90': '〉',
    'ã\x91': '《',
    'ã\x92': '》',
    'ã\x93': '〈',
    'ã\x94': '〉',
}

for garbled, correct in replacements.items():
    content = content.replace(garbled, correct)

# Also fix the template path
content = content.replace('clubs/cross_school_event_form.html', 'clubs/event_create.html')

# Write back
with open(r'D:\campus_club_site\clubs\views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed views.py')
