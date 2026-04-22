import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_club_site.settings')
import django
django.setup()

from clubs.models import CrossSchoolEvent

activities = CrossSchoolEvent.objects.all()
print(f'Total activities: {activities.count()}')
for a in activities:
    print(f'ID={a.id}, Title={a.title}, Creator={a.creator}, Club={a.club}')
