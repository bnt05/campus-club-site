# Fix views.py by properly handling encoding
import codecs

# Read the corrupted file
with open(r'D:\campus_club_site\clubs\views.py', 'rb') as f:
    raw = f.read()

# Try to decode as UTF-8 with error handling
try:
    content = raw.decode('utf-8')
    print("File decoded as UTF-8 successfully")
except:
    # If UTF-8 fails, try to understand the corruption pattern
    # The file was likely read as Latin-1 which corrupted multi-byte UTF-8 sequences
    content = raw.decode('latin-1')
    print("File decoded as Latin-1 - corruption detected")

# Save the raw bytes for analysis
with open(r'D:\campus_club_site\clubs\views_raw_backup.txt', 'wb') as f:
    f.write(raw)
print("Raw bytes saved for analysis")

# Check the file length
print(f"File has {len(content)} characters")
