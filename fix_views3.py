# Fix views.py
views_path = r'D:\campus_club_site\clubs\views.py'

with open(views_path, 'rb') as f:
    raw = f.read()

# Try to decode
try:
    content = raw.decode('utf-8')
except:
    content = raw.decode('latin-1')

# Fix template path
content = content.replace('clubs/cross_school_event_form.html', 'clubs/event_create.html')

# Fix common garbled patterns
content = content.replace('�?', '。')

with open(views_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
