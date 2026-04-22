import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_club_site.settings')
import django
django.setup()

from clubs.models import CrossSchoolEvent

try:
    e = CrossSchoolEvent.objects.get(id=2)
    print(f'Found activity: ID={e.id}, Title={e.title}, Creator={e.creator}, Club={e.club}')
    e.delete()
    print('Deleted successfully!')
except CrossSchoolEvent.DoesNotExist:
    print('Activity with ID 2 not found')
except Exception as e:
    print(f'Error: {e}')

# Verify deletion
print(f'\nRemaining activities: {CrossSchoolEvent.objects.count()}')
for a in CrossSchoolEvent.objects.all():
    print(f'ID={a.id}, Title={a.title}')
