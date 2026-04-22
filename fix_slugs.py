"""
Fix article slugs
"""
import os
import sys

sys.path.insert(0, r'D:\campus_club_site')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_club_site.settings')
import django
django.setup()

from clubs.models import EncyclopediaArticle


def fix_slugs():
    print('Fixing article slugs...')
    
    for article in EncyclopediaArticle.objects.all():
        old_slug = article.slug
        title = article.title
        
        # Generate new slug using pinyin
        try:
            from pypinyin import lazy_pinyin
            pinyin_list = lazy_pinyin(title)
            initials = ''.join([p[0].upper() if p and len(p) > 0 else 'X' for p in pinyin_list])
            new_slug = initials[:4]
        except:
            new_slug = f'ART{hash(title) % 10000}'
        
        # Ensure unique slug
        base_slug = new_slug
        counter = 1
        while EncyclopediaArticle.objects.filter(slug=new_slug).exclude(id=article.id).exists():
            new_slug = f'{base_slug}{counter}'
            counter += 1
        
        article.slug = new_slug
        article.save(update_fields=['slug'])
        print(f'  [{article.id}] {title}: {old_slug} -> {new_slug}')
    
    print('Done!')


if __name__ == '__main__':
    fix_slugs()
