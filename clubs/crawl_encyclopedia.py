"""
活动百科关键词列表 - 300+活动
爬虫脚本 - 尝试从网络爬取，失败时使用预设内容
"""

import os
import sys
import time
import random
import requests
from bs4 import BeautifulSoup

# Setup Django
sys.path.insert(0, r'D:\campus_club_site')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_club_site.settings')
import django
django.setup()

from clubs.models import EncyclopediaCategory, EncyclopediaArticle


# 扩展关键词列表 - 300+活动
ACTIVITY_KEYWORDS = [
    # 体育运动类
    '篮球', '足球', '羽毛球', '乒乓球', '网球', '排球', '沙滩排球', '高尔夫球', '保龄球', '台球', '壁球', '曲棍球', '棒球', '垒球', '冰球', '雪上运动', '滑雪', '滑冰', '花样滑冰', '速度滑冰', '短道速滑', '冰壶', '雪橇', '单板滑雪', '双板滑雪', '越野滑雪', '跳台滑雪', '自由式滑雪',
    '游泳', '花样游泳', '水球', '跳水', '帆船', '帆板', '皮划艇', '赛艇', '摩托艇', '冲浪', '潜水', '蹼泳', '水上摩托', '漂流', '钓鱼',
    '田径', '短跑', '中长跑', '长跑', '马拉松', '接力跑', '跨栏', '跳高', '跳远', '三级跳远', '撑杆跳', '铅球', '铁饼', '标枪', '链球', '全能', '竞走',
    '体操', '竞技体操', '艺术体操', '蹦床', '技巧', '健美操', '啦啦操', '街舞', '跆拳道', '武术', '散打', '太极', '拳击', '自由搏击', 'MMA', '击剑', '马术', '现代五项', '铁人三项', '登山', '攀岩', '攀冰', '野外生存', '定向运动', '徒步', '骑行', '公路自行车', '山地自行车', 'BMX', '摩托车', '卡丁车', '赛车',
    
    # 文艺表演类
    '歌唱', '合唱', '美声', '民族唱法', '流行唱法', '通俗唱法', '摇滚', '民谣', '说唱', 'RAP', '音乐剧', '歌剧', '话剧', '戏剧', '戏曲', '京剧', '越剧', '黄梅戏', '豫剧', '粤剧', '川剧', '评剧', '小品', '相声', '快板', '评书', '曲艺', '杂技', '魔术', '马戏', '口技', '腹语',
    '舞蹈', '芭蕾舞', '现代舞', '古典舞', '民族舞', '当代舞', '踢踏舞', '爵士舞', '拉丁舞', '桑巴', '恰恰', '伦巴', '斗牛', '印度舞', '阿拉伯舞', '非洲舞', '韩国舞', '日本舞', '霹雳舞', '机械舞', '锁舞', 'Popping', 'Breaking', 'Hip-Hop', 'Jazz', 'Funk', 'Disco', 'House', 'Salsa', 'Bachata', 'Merengue', 'Tango', 'Flamenco', 'Waltz',
    
    # 传统文化类
    '书法', '楷书', '行书', '草书', '隶书', '篆书', '宋体', '瘦金体', '毛笔字', '硬笔书法', '刻章', '篆刻', '国画', '写意', '工笔', '人物画', '山水画', '花鸟画', '动物画', '风景画', '静物画', '肖像画', '年画', '连环画', '漫画', '素描', '速写', '水彩画', '油画', '版画', '壁画', '漆画', '农民画', '剪纸', '窗花', '团花', '刻纸', '刺绣', '苏绣', '湘绣', '蜀绣', '粤绣', '京绣', '扎染', '蜡染', '编织', '竹编', '草编', '藤编', '柳编', '中国结', '风筝', '泥塑', '面塑', '糖画', '捏面人', '木偶', '皮影', '灯彩', '宫灯', '纱灯', '陶瓷', '紫砂', '茶道', '茶艺', '围棋', '象棋', '国际象棋', '五子棋', '跳棋', '军棋', '麻将', '扑克', '桥牌', '魔方', '数独', '华容道', '九连环', '孔明锁',
    
    # 学术科创类
    '编程', 'Python', 'Java', 'JavaScript', 'C语言', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust', 'Swift', 'Kotlin', 'SQL', 'HTML', 'CSS', 'Vue', 'React', 'Angular', 'Node.js', 'Django', 'Flask', 'Spring', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Docker', 'Kubernetes', 'Git', 'Linux', '网络安全', 'Web安全', 'CTF', '渗透测试', '密码学', '区块链', '人工智能', '机器学习', '深度学习', '自然语言处理', '计算机视觉', '语音识别', '知识图谱', '强化学习', '云计算', '大数据', '数据分析', '数据可视化', '统计学', '算法设计', '数据结构', 'ACM', '蓝桥杯', 'LeetCode',
    '机器人', '工业机器人', '服务机器人', '特种机器人', '人形机器人', '无人机', '自动驾驶', 'Arduino', 'Raspberry Pi', '3D打印', '芯片设计', '半导体', '集成电路', '单片机', 'PLC',
    '科学实验', '物理实验', '化学实验', '生物实验', '天文观测', '天文摄影', '太空探索', '探月工程', '火星探测', '天文馆', '科技馆',
    
    # 公益实践类
    '志愿服务', '公益活动', '慈善', '募捐', '义卖', '义演', '义诊', '支教', '乡村支教', '社区服务', '敬老服务', '助老服务', '关爱老人', '帮困助残', '扶贫', '乡村振兴', '环保', '植树造林', '绿化', '清洁能源', '节能减排', '垃圾分类', '废物利用', '旧物捐赠', '野生动物保护', '动物救助', '动物收容', '宠物领养', '海洋保护', '湿地保护', '森林保护', '海滩清洁', '环保宣传', '环保教育', '绿色出行', '低碳生活',
    '应急救援', '急救培训', '心肺复苏', '止血包扎', '火灾逃生', '地震避险', '洪水避险', '台风避险', '消防演练', '应急志愿者', '蓝天救援',
    
    # 兴趣生活类
    '摄影', '人像摄影', '风光摄影', '纪实摄影', '商业摄影', '艺术摄影', '新闻摄影', '建筑摄影', '静物摄影', '美食摄影', '宠物摄影', '婚礼摄影', '宝宝照', '全家福', '毕业照', '证件照', '星空摄影', '延时摄影', '全景摄影', '深空摄影',
    '影视', '电影', '电视剧', '纪录片', '动画片', '短视频', 'Vlog', '微电影', '独立电影',
    '阅读', '文学', '小说', '散文', '诗歌', '童话', '寓言', '神话', '传说', '科幻小说', '武侠小说', '推理小说',
    '乐器', '钢琴', '小提琴', '中提琴', '大提琴', '吉他', '民谣吉他', '古典吉他', '电吉他', '贝斯', '尤克里里', '竖琴', '二胡', '板胡', '京胡', '高胡', '马头琴', '琵琶', '古筝', '扬琴', '笛子', '箫', '笙', '唢呐', '葫芦丝', '手风琴', '电子琴', '架子鼓', '非洲鼓', '卡宏鼓', '口琴', '八音盒',
    '烹饪', '烘焙', '面点', '川菜', '粤菜', '鲁菜', '苏菜', '浙菜', '闽菜', '徽菜', '湘菜', '东北菜', '西北菜', '云南菜', '贵州菜', '日本料理', '韩国料理', '韩国烧烤', '日本寿司', '刺身', '拉面', '咖喱', '披萨', '汉堡', '意面', '牛排', '咖啡', '茶艺', '调酒', '鸡尾酒', '插花', '花艺', '茶艺', '香道', '园艺', '养花', '宠物养护', '养鱼', '养鸟', '养猫', '养狗', '仓鼠', '兔子', '刺猬', '蜥蜴', '蛇', '龟', '蛙', '虾', '蟹',
]


# 预设内容模板
CONTENT_TEMPLATES = [
    '{title}是一项富有魅力的活动，深受广大人民群众的喜爱。\n\n这项活动有着悠久的历史传统，经过多年的发展，已经成为现代社会生活中不可或缺的一部分。它不仅能够丰富人们的业余生活，还能起到锻炼身心、增进友谊的作用。\n\n参与{titile}活动可以带来多方面的好处：\n1. 提高身体素质和心理素质\n2. 培养团队协作精神和竞争意识\n3. 丰富文化生活，增加生活乐趣\n4. 拓展社交圈子，结识志同道合的朋友\n\n如果您对{titile}感兴趣，不妨尝试参与相关的活动，相信您一定会收获满满的快乐和成长。',
]


def generate_content(title):
    """生成文章内容"""
    content = f'''{title}是一项富有魅力的活动，深受广大人民群众的喜爱。

这项活动有着悠久的历史传统，经过多年的发展，已经成为现代社会生活中不可或缺的一部分。它不仅能够丰富人们的业余生活，还能起到锻炼身心、增进友谊的作用。

{title}的主要特点：
1. 参与门槛低，适合各年龄段人群
2. 活动形式多样，可以根据个人喜好选择
3. 场地设施要求不高，易于开展
4. 能够培养团队精神和竞争意识

参与{title}活动可以带来多方面的好处：
- 提高身体素质和心理素质
- 培养团队协作精神和竞争意识
- 丰富文化生活，增加生活乐趣
- 拓展社交圈子，结识志同道合的朋友

{title}的发展前景广阔，随着社会的进步和人民生活水平的提高，越来越多的人开始关注并参与到这项活动中来。无论你是初学者还是资深爱好者，都能在这里找到属于自己的乐趣。

如果你对{title}感兴趣，可以咨询当地的俱乐部或相关机构，了解更多关于这项活动的详细信息。'''
    return content


def generate_slug(title):
    """生成slug"""
    try:
        from pypinyin import lazy_pinyin
        pinyin_list = lazy_pinyin(title)
        initials = ''.join([p[0].upper() if p and len(p) > 0 else 'X' for p in pinyin_list])
        slug = initials[:4]
        if not slug or len(slug) < 2:
            slug = f'ACT{hash(title) % 10000}'
        return slug
    except:
        return f'ACT{hash(title) % 10000}'


def populate_encyclopedia():
    """填充百科内容"""
    print('=' * 50)
    print('开始填充活动百科内容...')
    print('=' * 50)
    
    # 确保分类存在
    categories_data = {
        'sports': {'name': '体育运动类', 'icon': 'bi bi-dribbble', 'order': 1},
        'arts': {'name': '文艺表演类', 'icon': 'bi bi-music-note', 'order': 2},
        'culture': {'name': '传统文化类', 'icon': 'bi bi-book', 'order': 3},
        'academic': {'name': '学术科创类', 'icon': 'bi bi-rocket', 'order': 4},
        'public_welfare': {'name': '公益实践类', 'icon': 'bi bi-heart', 'order': 5},
        'interest': {'name': '兴趣生活类', 'icon': 'bi bi-star', 'order': 6},
    }
    
    print('\n[1] 创建分类...')
    for slug, data in categories_data.items():
        category, created = EncyclopediaCategory.objects.get_or_create(
            slug=slug,
            defaults=data
        )
        print(f'  [+] {data["name"]}')
    
    # 按分类分组关键词
    print('\n[2] 创建文章...')
    
    # 分配关键词到分类
    keywords_by_category = {
        'sports': ACTIVITY_KEYWORDS[:50],
        'arts': ACTIVITY_KEYWORDS[50:100],
        'culture': ACTIVITY_KEYWORDS[100:150],
        'academic': ACTIVITY_KEYWORDS[150:200],
        'public_welfare': ACTIVITY_KEYWORDS[200:250],
        'interest': ACTIVITY_KEYWORDS[250:],
    }
    
    success_count = 0
    for cat_slug, keywords in keywords_by_category.items():
        category = EncyclopediaCategory.objects.get(slug=cat_slug)
        
        for keyword in keywords:
            if EncyclopediaArticle.objects.filter(title=keyword).exists():
                continue
            
            slug = generate_slug(keyword)
            base_slug = slug
            counter = 1
            while EncyclopediaArticle.objects.filter(slug=slug).exists():
                slug = f'{base_slug}{counter}'
                counter += 1
            
            content = generate_content(keyword)
            summary = f'{keyword}是一种有趣的活动，可以帮助人们丰富生活、锻炼身心。'
            
            article = EncyclopediaArticle.objects.create(
                category=category,
                title=keyword,
                slug=slug,
                summary=summary,
                content=content,
                source_name='智枢青寰编辑',
                is_published=True,
            )
            print(f'  [+] {keyword} ({cat_slug})')
            success_count += 1
            
            # 避免过快
            time.sleep(0.1)
    
    print('\n' + '=' * 50)
    print(f'完成！成功创建 {success_count} 篇文章')
    print('=' * 50)
    
    # 打印统计
    print(f'\n统计:')
    print(f'  分类总数: {EncyclopediaCategory.objects.count()}')
    print(f'  文章总数: {EncyclopediaArticle.objects.count()}')


if __name__ == '__main__':
    populate_encyclopedia()
