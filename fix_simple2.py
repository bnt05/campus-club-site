# Fix views.py - simplified approach
with open(r'D:\campus_club_site\clubs\views.py', 'rb') as f:
    raw = f.read()

content = raw.decode('utf-8', errors='replace')

# Template path fix
content = content.replace('clubs/cross_school_event_form.html', 'clubs/event_create.html')

# Fix common garbled patterns (from Latin-1 mojibake)
replacements = [
    ('\xc3\xa4\xc2\xb8\xc2\xac', '\xe5\x8f\xaf'),
    ('\xc3\xa4\xc2\xb8\xc2\xad', '\xe5\x8f\xaf'),
    ('\xc3\xa6\xc2\x88\xc2\x90', '\xe7\xa6\x81'),
    ('\xc3\xa5\xc2\x8a\xc2\x8c', '\xe5\x8a\x9f'),
    ('\xc3\xa5\xc2\x8a\xc2\x8f', '\xe5\x8a\xaf'),
    ('\xc3\xa4\xc2\xb8\xc2\xaa', '\xe4\xbb\xac'),
    ('\xc3\xa4\xc2\xb8\xc2\xac', '\xe4\xb8\xaa'),
    ('\xc3\xa4\xc2\xb8\xc2\xad', '\xe4\xb8\xad'),
    ('\xc3\xa4\xc2\xb8\xc2\xaf', '\xe4\xb8\xaf'),
    ('\xc3\xa5\xc2\x8f\xc2\x9f', '\xe5\x8f\xb0'),
    ('\xc3\xa5\xc2\x8e\xc2\xad', '\xe5\x8e\x8b'),
    ('\xc3\xa4\xc2\xb8\xc2\x89', '\xe4\xb8\x89'),
]

for old, new in replacements:
    try:
        old_str = old.decode('latin-1')
        new_str = new.decode('utf-8')
        content = content.replace(old_str, new_str)
    except:
        pass

with open(r'D:\campus_club_site\clubs\views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
