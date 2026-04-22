# Simple fix for views.py
with open(r'D:\campus_club_site\clubs\views.py', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

content = content.replace('clubs/cross_school_event_form.html', 'clubs/event_create.html')

with open(r'D:\campus_club_site\clubs\views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
