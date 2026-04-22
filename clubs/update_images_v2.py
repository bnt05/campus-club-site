"""
更完善地更新百科文章图片 - 使用分类+关键词匹配
"""
import os
import sys

sys.path.insert(0, r'D:\campus_club_site')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_club_site.settings')
import django
django.setup()

from clubs.models import EncyclopediaArticle


# 按分类的图片URL
CATEGORY_IMAGES = {
    'sports': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800',
    'arts': 'https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=800',
    'culture': 'https://images.unsplash.com/photo-1517971129774-8a2d38d3e37d?w=800',
    'academic': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800',
    'public_welfare': 'https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=800',
    'interest': 'https://images.unsplash.com/photo-1452587925148-ce544e77e70d?w=800',
}


def get_relevant_image(title, category_slug):
    """根据标题和分类获取相关图片"""
    title_lower = title.lower()
    
    # 体育类关键词
    if category_slug == 'sports':
        sports_keywords = {
            '篮球': 'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=800',
            '足球': 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=800',
            '羽毛球': 'https://images.unsplash.com/photo-1599256621730-0fd2443623ed?w=800',
            '乒乓': 'https://images.unsplash.com/photo-1534158914592-062992fbe609?w=800',
            '网球': 'https://images.unsplash.com/photo-1554068865-24cecd4e54b8?w=800',
            '排球': 'https://images.unsplash.com/photo-1612872087720-bb876e2e4d14?w=800',
            '游泳': 'https://images.unsplash.com/photo-1560090995-01632a28895b?w=800',
            '体操': 'https://images.unsplash.com/photo-1526232761682-d26e03ac148e?w=800',
            '武术': 'https://images.unsplash.com/photo-1544367567-0f2fe5c74c6b?w=800',
            '太极': 'https://images.unsplash.com/photo-1544367567-0f2fe5c74c6b?w=800',
            '拳击': 'https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?w=800',
            '跆拳道': 'https://images.unsplash.com/photo-1555597673-b411d2dd7f0a?w=800',
            '登山': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800',
            '攀岩': 'https://images.unsplash.com/photo-1522163182402-834f871fd851?w=800',
            '瑜伽': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800',
            '舞蹈': 'https://images.unsplash.com/photo-1508700929628-555bc8c8bde5?w=800',
            '田径': 'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=800',
            '马拉松': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',
            '骑行': 'https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=800',
            '滑雪': 'https://images.unsplash.com/photo-1551698618-1dfe5d97d256?w=800',
            '滑冰': 'https://images.unsplash.com/photo-1517866405746-2b5d8c8b7f7e?w=800',
            '潜水': 'https://images.unsplash.com/photo-1544551763-77ef2d0cfc6c?w=800',
            '冲浪': 'https://images.unsplash.com/photo-1502680390546-bbf11e7e6f2?w=800',
            '帆船': 'https://images.unsplash.com/photo-1500514966906-fe245eea9344?w=800',
            '钓鱼': 'https://images.unsplash.com/photo-1504472478169-9367595e9e76?w=800',
        }
        for kw, url in sports_keywords.items():
            if kw in title:
                return url
        return CATEGORY_IMAGES['sports']
    
    # 文艺类关键词
    elif category_slug == 'arts':
        arts_keywords = {
            '歌唱': 'https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=800',
            '合唱': 'https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=800',
            '钢琴': 'https://images.unsplash.com/photo-1520523839897-bd0b52f945a0?w=800',
            '吉他': 'https://images.unsplash.com/photo-1510915361894-db8b60106cb1?w=800',
            '小提琴': 'https://images.unsplash.com/photo-1465847899084-d164df4dedc6?w=800',
            '架子鼓': 'https://images.unsplash.com/photo-1519892300165-cb5542bc47d0?w=800',
            '舞蹈': 'https://images.unsplash.com/photo-1508700929628-555bc8c8bde5?w=800',
            '芭蕾': 'https://images.unsplash.com/photo-1518834107812-67b0b7c5843e?w=800',
            '京剧': 'https://images.unsplash.com/photo-1591122947157-26bad3a117e5?w=800',
            '戏剧': 'https://images.unsplash.com/photo-1508700929628-555bc8c8bde5?w=800',
            '相声': 'https://images.unsplash.com/photo-1508700929628-555bc8c8bde5?w=800',
            '杂技': 'https://images.unsplash.com/photo-1508700929628-555bc8c8bde5?w=800',
            '魔术': 'https://images.unsplash.com/photo-1508700929628-555bc8c8bde5?w=800',
        }
        for kw, url in arts_keywords.items():
            if kw in title:
                return url
        return CATEGORY_IMAGES['arts']
    
    # 文化类关键词
    elif category_slug == 'culture':
        culture_keywords = {
            '书法': 'https://images.unsplash.com/photo-1517971129774-8a2d38d3e37d?w=800',
            '国画': 'https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?w=800',
            '素描': 'https://images.unsplash.com/photo-1513364776144-60967b0f7f83?w=800',
            '油画': 'https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?w=800',
            '水彩': 'https://images.unsplash.com/photo-1513364776144-60967b0f7f83?w=800',
            '剪纸': 'https://images.unsplash.com/photo-1604431698585-e379a78a8d0c?w=800',
            '刺绣': 'https://images.unsplash.com/photo-1604431698585-e379a78a8d0c?w=800',
            '陶瓷': 'https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?w=800',
            '茶道': 'https://images.unsplash.com/photo-1544787219-0fd2443623ed?w=800',
            '围棋': 'https://images.unsplash.com/photo-1529699211952-734e80c4d18b?w=800',
            '象棋': 'https://images.unsplash.com/photo-1529699211952-734e80c4d18b?w=800',
            '麻将': 'https://images.unsplash.com/photo-1529699211952-734e80c4d18b?w=800',
            '魔方': 'https://images.unsplash.com/photo-1552527806-33776ac54e76?w=800',
        }
        for kw, url in culture_keywords.items():
            if kw in title:
                return url
        return CATEGORY_IMAGES['culture']
    
    # 学术科创类关键词
    elif category_slug == 'academic':
        academic_keywords = {
            '编程': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800',
            '人工智能': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800',
            '机器人': 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800',
            '3D打印': 'https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=800',
            '天文': 'https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=800',
            '科学实验': 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=800',
            '化学实验': 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=800',
            '物理实验': 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=800',
            '生物实验': 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=800',
            '无人机': 'https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=800',
            '自动驾驶': 'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800',
        }
        for kw, url in academic_keywords.items():
            if kw in title:
                return url
        return CATEGORY_IMAGES['academic']
    
    # 公益实践类关键词
    elif category_slug == 'public_welfare':
        pw_keywords = {
            '志愿': 'https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=800',
            '公益': 'https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=800',
            '慈善': 'https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=800',
            '支教': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800',
            '敬老': 'https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=800',
            '环保': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800',
            '植树': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800',
            '急救': 'https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=800',
            '应急': 'https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=800',
        }
        for kw, url in pw_keywords.items():
            if kw in title:
                return url
        return CATEGORY_IMAGES['public_welfare']
    
    # 兴趣生活类关键词
    elif category_slug == 'interest':
        interest_keywords = {
            '摄影': 'https://images.unsplash.com/photo-1452587925148-ce544e77e70d?w=800',
            '电影': 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800',
            '阅读': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800',
            '文学': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800',
            '烹饪': 'https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=800',
            '烘焙': 'https://images.unsplash.com/photo-1486427944299-d1955e23bc4d?w=800',
            '咖啡': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800',
            '茶艺': 'https://images.unsplash.com/photo-1544787219-0fd2443623ed?w=800',
            '宠物': 'https://images.unsplash.com/photo-1474511320723-9a56873571b7?w=800',
            '养猫': 'https://images.unsplash.com/photo-1514888286974-4c1362afd8b6?w=800',
            '养狗': 'https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=800',
            '旅行': 'https://images.unsplash.com/photo-1488085061387-422e29b4003a?w=800',
            '自驾': 'https://images.unsplash.com/photo-1488085061387-422e29b4003a?w=800',
            '露营': 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=800',
        }
        for kw, url in interest_keywords.items():
            if kw in title:
                return url
        return CATEGORY_IMAGES['interest']
    
    return 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800'


def update_images():
    print('=' * 60)
    print('开始更新百科文章图片（分类+关键词匹配）...')
    print('=' * 60)
    
    articles = EncyclopediaArticle.objects.all()
    updated = 0
    
    for article in articles:
        new_image = get_relevant_image(article.title, article.category.slug)
        article.image_url = new_image
        article.save(update_fields=['image_url'])
        updated += 1
        if updated <= 30:
            print(f'  [{updated}] {article.title} ({article.category.name})')
    
    print(f'\n共更新 {updated} 篇文章的图片')
    print('=' * 60)


if __name__ == '__main__':
    update_images()
