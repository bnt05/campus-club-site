"""
更新百科文章图片
"""
import os
import sys

sys.path.insert(0, r'D:\campus_club_site')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_club_site.settings')
import django
django.setup()

from clubs.models import EncyclopediaArticle


# 关键词到相关图片URL的映射
IMAGE_MAP = {
    '篮球': 'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=800',
    '足球': 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=800',
    '羽毛球': 'https://images.unsplash.com/photo-1599256621730-0fd2443623ed?w=800',
    '乒乓球': 'https://images.unsplash.com/photo-1534158914592-062992fbe609?w=800',
    '网球': 'https://images.unsplash.com/photo-1554068865-24cecd4e54b8?w=800',
    '排球': 'https://images.unsplash.com/photo-1612872087720-bb876e2e4d14?w=800',
    '游泳': 'https://images.unsplash.com/photo-1560090995-01632a28895b?w=800',
    '跳水': 'https://images.unsplash.com/photo-1506252374453-ef5237291d83?w=800',
    '体操': 'https://images.unsplash.com/photo-1526232761682-d26e03ac148e?w=800',
    '武术': 'https://images.unsplash.com/photo-1544367567-0f2fe5c74c6b?w=800',
    '太极拳': 'https://images.unsplash.com/photo-1544367567-0f2fe5c74c6b?w=800',
    '拳击': 'https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?w=800',
    '登山': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800',
    '攀岩': 'https://images.unsplash.com/photo-1522163182402-834f871fd851?w=800',
    '骑行': 'https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=800',
    '瑜伽': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800',
    '舞蹈': 'https://images.unsplash.com/photo-1508700929628-555bc8c8bde5?w=800',
    '芭蕾舞': 'https://images.unsplash.com/photo-1518834107812-67b0b7c5843e?w=800',
    '歌唱': 'https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=800',
    '钢琴演奏': 'https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=800',
    '吉他弹奏': 'https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=800',
    '架子鼓演奏': 'https://images.unsplash.com/photo-1519892300165-cb5542bc47d0?w=800',
    '书法': 'https://images.unsplash.com/photo-1517971129774-8a2d38d3e37d?w=800',
    '国画': 'https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?w=800',
    '素描': 'https://images.unsplash.com/photo-1513364776144-60967b0f7f83?w=800',
    '剪纸': 'https://images.unsplash.com/photo-1604431698585-e379a78a8d0c?w=800',
    '陶瓷': 'https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?w=800',
    '茶道': 'https://images.unsplash.com/photo-1544787219-0fd2443623ed?w=800',
    '围棋': 'https://images.unsplash.com/photo-1529699211952-734e80c4d18b?w=800',
    '象棋': 'https://images.unsplash.com/photo-1529699211952-734e80c4d18b?w=800',
    '魔方': 'https://images.unsplash.com/photo-1552527806-33776ac54e76?w=800',
    '编程开发': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800',
    '人工智能': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800',
    '机器人技术': 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800',
    '摄影艺术': 'https://images.unsplash.com/photo-1452587925148-ce544e77e70d?w=800',
    '烹饪技术': 'https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=800',
    '咖啡制作': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800',
    '志愿服务': 'https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=800',
    '环保行动': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800',
}


def get_relevant_image(title):
    if title in IMAGE_MAP:
        return IMAGE_MAP[title]
    for keyword, url in IMAGE_MAP.items():
        if keyword in title or title in keyword:
            return url
    return 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800'


def update_images():
    print('=' * 50)
    print('开始更新百科文章图片...')
    print('=' * 50)
    
    articles = EncyclopediaArticle.objects.all()
    updated = 0
    
    for article in articles:
        new_image = get_relevant_image(article.title)
        article.image_url = new_image
        article.save(update_fields=['image_url'])
        updated += 1
        if updated <= 20:
            print(f'  [{updated}] {article.title} -> {new_image[-40:]}')
    
    print(f'\n共更新 {updated} 篇文章的图片')
    print('=' * 50)


if __name__ == '__main__':
    update_images()
