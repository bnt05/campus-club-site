"""
从百度百科爬取活动相关词条内容
"""
import os
import sys

# Setup Django
sys.path.insert(0, r'D:\campus_club_site')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_club_site.settings')
import django
django.setup()

import requests
from bs4 import BeautifulSoup
import re
import time

# 活动词条列表（可以自行添加更多）
ACTIVITY_KEYWORDS = [
    '书法', '剪纸', '篮球', '足球', '羽毛球', '乒乓球', '网球', '保龄球',
    '舞蹈', '歌唱', '朗诵', '演讲', '辩论', '摄影', '绘画', '陶艺',
    '志愿者', '支教', '环保', '科技', '编程', '机器人', '3D打印',
    '马拉松', '游泳', '跆拳道', '武术', '瑜伽', '登山', '骑行',
    '电影', '戏剧', '音乐', '乐器', '合唱', '街舞', '拉丁舞',
    '插花', '茶道', '香道', '围棋', '象棋', '桥牌', '魔方',
    '科学实验', '天文', '地理', '历史', '文学', '外语',
]

CATEGORY_MAP = {
    '书法': {'category': 'culture', 'icon': 'bi bi-brush'},
    '剪纸': {'category': 'culture', 'icon': 'bi bi-scissors'},
    '篮球': {'category': 'sports', 'icon': 'bi bi-dribbble'},
    '足球': {'category': 'sports', 'icon': 'bi bi-soccer'},
    '羽毛球': {'category': 'sports', 'icon': 'bi bi-circle'},
    '乒乓球': {'category': 'sports', 'icon': 'bi bi-circle'},
    '网球': {'category': 'sports', 'icon': 'bi bi-circle'},
    '保龄球': {'category': 'sports', 'icon': 'bi bi-circle'},
    '舞蹈': {'category': 'arts', 'icon': 'bi bi-music-note'},
    '歌唱': {'category': 'arts', 'icon': 'bi bi-mic'},
    '朗诵': {'category': 'arts', 'icon': 'bi bi-megaphone'},
    '演讲': {'category': 'arts', 'icon': 'bi bi-megaphone'},
    '辩论': {'category': 'academic', 'icon': 'bi bi-chat-quote'},
    '摄影': {'category': 'arts', 'icon': 'bi bi-camera'},
    '绘画': {'category': 'arts', 'icon': 'bi bi-palette'},
    '陶艺': {'category': 'arts', 'icon': 'bi bi-cup'},
    '志愿者': {'category': 'public_welfare', 'icon': 'bi bi-heart'},
    '支教': {'category': 'public_welfare', 'icon': 'bi bi-mortarboard'},
    '环保': {'category': 'public_welfare', 'icon': 'bi bi-tree'},
    '科技': {'category': 'academic', 'icon': 'bi bi-rocket'},
    '编程': {'category': 'academic', 'icon': 'bi bi-code'},
    '机器人': {'category': 'academic', 'icon': 'bi bi-robot'},
    '3D打印': {'category': 'academic', 'icon': 'bi bi-box'},
    '马拉松': {'category': 'sports', 'icon': 'bi bi-person'},
    '游泳': {'category': 'sports', 'icon': 'bi bi-water'},
    '跆拳道': {'category': 'sports', 'icon': 'bi bi-person'},
    '武术': {'category': 'sports', 'icon': 'bi bi-person'},
    '瑜伽': {'category': 'sports', 'icon': 'bi bi-person'},
    '登山': {'category': 'sports', 'icon': 'bi bi-mountain'},
    '骑行': {'category': 'sports', 'icon': 'bi bi-bicycle'},
    '电影': {'category': 'arts', 'icon': 'bi bi-film'},
    '戏剧': {'category': 'arts', 'icon': 'bi bi-mask'},
    '音乐': {'category': 'arts', 'icon': 'bi bi-music-note-list'},
    '乐器': {'category': 'arts', 'icon': 'bi bi-music-note-list'},
    '合唱': {'category': 'arts', 'icon': 'bi bi-people'},
    '街舞': {'category': 'arts', 'icon': 'bi bi-person'},
    '拉丁舞': {'category': 'arts', 'icon': 'bi bi-person'},
    '插花': {'category': 'interest', 'icon': 'bi bi-flower'},
    '茶道': {'category': 'interest', 'icon': 'bi bi-cup'},
    '香道': {'category': 'interest', 'icon': 'bi bi-wind'},
    '围棋': {'category': 'interest', 'icon': 'bi bi-grid'},
    '象棋': {'category': 'interest', 'icon': 'bi bi-grid'},
    '桥牌': {'category': 'interest', 'icon': 'bi bi-grid'},
    '魔方': {'category': 'interest', 'icon': 'bi bi-grid-3x3'},
    '科学实验': {'category': 'academic', 'icon': 'bi bi-flask'},
    '天文': {'category': 'academic', 'icon': 'bi bi-stars'},
    '地理': {'category': 'academic', 'icon': 'bi bi-globe'},
    '历史': {'category': 'academic', 'icon': 'bi bi-book'},
    '文学': {'category': 'academic', 'icon': 'bi bi-book'},
    '外语': {'category': 'academic', 'icon': 'bi bi-globe2'},
}


def slugify(text):
    """将中文转换为拼音slug"""
    from pypinyin import lazy_pinyin
    pinyin_list = lazy_pinyin(text)
    slug = ''.join(pinyin_list)
    # 清理特殊字符
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    return slug[:50]


def fetch_baidu_baike(keyword):
    """
    从百度百科获取词条内容
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    url = f'https://baike.baidu.com/item/{keyword}'
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            return response.text
        else:
            print(f'  [!] 请求失败: {keyword}, 状态码: {response.status_code}')
            return None
    except Exception as e:
        print(f'  [!] 请求异常: {keyword}, 错误: {e}')
        return None


def parse_baidu_baike(html_content, keyword):
    """
    解析百度百科页面，提取内容
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 提取标题
    title = soup.find('h1', class_='lemmaTitle')
    if not title:
        title = soup.find('h1')
    title_text = title.get_text(strip=True) if title else keyword
    
    # 提取摘要
    summary = ''
    summary_div = soup.find('div', class_='lemma-summary')
    if summary_div:
        # 移除参考来源标记
        for sup in summary_div.find_all('sup'):
            sup.decompose()
        for a in summary_div.find_all('a'):
            if a.get('href'):
                a.unwrap()
        summary = summary_div.get_text(strip=True)
    
    # 提取正文内容
    content = []
    content_div = soup.find('div', class_='lemma-content')
    if content_div:
        # 移除不需要的元素
        for elem in content_div.find_all(['script', 'style', 'sup', 'div', 'table']):
            elem.decompose()
        
        # 处理段落
        for p in content_div.find_all(['p', 'h2', 'h3', 'h4']):
            text = p.get_text(strip=True)
            if text and len(text) > 10:
                content.append(text)
    
    return {
        'title': title_text,
        'summary': summary[:500] if summary else '',
        'content': '\n\n'.join(content[:20]),  # 最多20段
    }


def crawl_baidu_baike():
    """
    主爬取函数
    """
    print('=' * 50)
    print('开始从百度百科爬取活动词条...')
    print('=' * 50)
    
    # 检查依赖
    try:
        import pypinyin
    except ImportError:
        print('[!] 缺少 pypinyin 库，请运行: pip install pypinyin')
        return
    
    try:
        from clubs.models import EncyclopediaCategory, EncyclopediaArticle
    except ImportError as e:
        print(f'[!] 无法导入模型: {e}')
        return
    
    # 确保分类存在
    categories_data = {
        'sports': ('体育竞技类', 'bi bi-dribbble'),
        'arts': ('文艺表演类', 'bi bi-music-note'),
        'culture': ('传统文化类', 'bi bi-book'),
        'academic': ('学术科创类', 'bi bi-rocket'),
        'public_welfare': ('公益实践类', 'bi bi-heart'),
        'interest': ('兴趣生活类', 'bi bi-star'),
    }
    
    for slug, (name, icon) in categories_data.items():
        category, created = EncyclopediaCategory.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'icon': icon,
                'order': list(categories_data.keys()).index(slug),
            }
        )
        if created:
            print(f'[+] 创建分类: {name}')
    
    # 爬取每个关键词
    success_count = 0
    for keyword in ACTIVITY_KEYWORDS:
        print(f'\n[*] 正在爬取: {keyword}...')
        
        # 检查是否已存在
        existing = EncyclopediaArticle.objects.filter(title=keyword).first()
        if existing:
            print(f'  [=] 已存在，跳过: {keyword}')
            continue
        
        # 爬取内容
        html = fetch_baidu_baike(keyword)
        if not html:
            continue
        
        # 解析内容
        data = parse_baidu_baike(html, keyword)
        
        if not data['content']:
            print(f'  [!] 未能提取到内容: {keyword}')
            continue
        
        # 确定分类
        cat_info = CATEGORY_MAP.get(keyword, {'category': 'interest', 'icon': 'bi bi-star'})
        category = EncyclopediaCategory.objects.filter(slug=cat_info['category']).first()
        if not category:
            category = EncyclopediaCategory.objects.filter(slug='interest').first()
        
        # 生成slug
        slug = slugify(keyword)
        # 确保slug唯一
        base_slug = slug
        counter = 1
        while EncyclopediaArticle.objects.filter(slug=slug).exists():
            slug = f'{base_slug}-{counter}'
            counter += 1
        
        # 创建文章
        article = EncyclopediaArticle.objects.create(
            category=category,
            title=data['title'],
            slug=slug,
            summary=data['summary'] or f'关于{data["title"]}的详细介绍',
            content=data['content'],
            source_url=f'https://baike.baidu.com/item/{keyword}',
            source_name='百度百科',
            is_published=True,
        )
        
        print(f'  [+] 创建成功: {article.title} (ID: {article.id})')
        success_count += 1
        
        # 礼貌性延迟
        time.sleep(1)
    
    print('\n' + '=' * 50)
    print(f'完成！成功创建 {success_count} 篇文章')
    print('=' * 50)


if __name__ == '__main__':
    crawl_baidu_baike()
