"""
重新生成纯中文百科内容
"""
import os
import sys
import time

sys.path.insert(0, r'D:\campus_club_site')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_club_site.settings')
import django
django.setup()

from clubs.models import EncyclopediaCategory, EncyclopediaArticle


# 纯中文关键词
KEYWORDS_BY_CATEGORY = {
    'sports': [
        '篮球', '足球', '羽毛球', '乒乓球', '网球', '排球', '沙滩排球', '高尔夫球', '保龄球', '台球',
        '壁球', '曲棍球', '棒球', '垒球', '冰球', '滑雪', '滑冰', '花样滑冰', '速度滑冰', '短道速滑',
        '冰壶', '雪橇', '游泳', '跳水', '水球', '帆船', '帆板', '皮划艇', '赛艇', '冲浪',
        '潜水', '钓鱼', '田径', '短跑', '中长跑', '长跑', '马拉松', '跨栏', '跳高', '跳远',
        '三级跳远', '撑杆跳', '铅球', '铁饼', '标枪', '体操', '艺术体操', '蹦床', '健美操', '街舞',
        '跆拳道', '武术', '散打', '太极拳', '拳击', '击剑', '马术', '登山', '攀岩', '野外生存',
        '定向运动', '徒步', '骑行', '拓展训练', '毽球', '门球', '板球', '橄榄球'
    ],
    'arts': [
        '歌唱', '合唱', '美声', '民族唱法', '流行唱法', '摇滚', '民谣', '说唱', '音乐剧', '歌剧',
        '话剧', '戏剧', '京剧', '越剧', '黄梅戏', '豫剧', '粤剧', '川剧', '评剧', '小品',
        '相声', '杂技', '魔术', '舞蹈', '芭蕾舞', '现代舞', '古典舞', '民族舞', '爵士舞', '拉丁舞',
        '桑巴舞', '恰恰舞', '伦巴舞', '斗牛舞', '瑜伽', '钢琴演奏', '小提琴演奏', '吉他弹奏', '架子鼓演奏',
        '二胡演奏', '琵琶演奏', '古筝演奏', '笛子吹奏', '萨克斯演奏', '手风琴演奏', '口琴演奏'
    ],
    'culture': [
        '书法', '楷书', '行书', '草书', '隶书', '篆书', '国画', '写意画', '工笔画', '人物画',
        '山水画', '花鸟画', '素描', '水彩画', '油画', '版画', '壁画', '剪纸', '窗花', '刺绣',
        '编织', '竹编', '草编', '中国结', '风筝', '泥塑', '面塑', '木偶', '皮影', '陶瓷',
        '紫砂', '青瓷', '茶道', '茶艺', '围棋', '象棋', '国际象棋', '五子棋', '麻将', '扑克牌',
        '魔方', '香道', '插花', '花艺', '香道文化'
    ],
    'academic': [
        '编程开发', '机器人技术', '人工智能', '机器学习', '深度学习', '大数据分析', '云计算技术',
        '网络安全', 'Web开发', '数据库管理', '算法设计', '数据结构', '电子制作', '3D打印技术',
        '航空航天知识', '天文观测', '天文摄影', '科学实验', '物理实验', '化学实验', '生物实验',
        '地理考察', '气象观测', '地震监测', '矿石标本', '植物学研究', '动物学研究', '微生物学',
        '化学工程', '材料科学', '纳米技术', '生物工程', '基因工程', '环境保护技术', '新能源技术',
        '核能技术', '太阳能技术', '风能技术', '地热能技术', '海洋技术', '测绘技术', '遥感技术',
        '北斗导航', '物联网技术', '区块链技术', '虚拟现实', '增强现实', '无人机技术', '自动驾驶技术'
    ],
    'public_welfare': [
        '志愿服务', '公益活动', '慈善捐赠', '义演义卖', '支教活动', '社区服务', '敬老服务', '助残服务',
        '扶贫活动', '环保行动', '植树造林', '垃圾分类', '野生动物保护', '动物救助', '海洋保护',
        '湿地保护', '森林保护', '河流保护', '应急救援', '急救培训', '消防演练', '心理援助',
        '无偿献血', '骨髓捐献', '器官捐献', '关爱留守儿童', '关爱空巢老人', '关爱农民工', '关爱贫困学生',
        '法律援助', '科普宣传', '文化下乡', '卫生下乡', '科技下乡', '社区志愿服务', '环保科普'
    ],
    'interest': [
        '摄影艺术', '人像摄影', '风光摄影', '纪实摄影', '微距摄影', '天文摄影', '建筑摄影', '美食摄影',
        '宠物摄影', '婚礼摄影', '电影观赏', '电视剧观赏', '纪录片观赏', '动画片观赏', '短视频制作',
        '阅读', '文学创作', '诗歌创作', '小说写作', '散文写作', '烹饪技术', '烘焙技术', '面点制作',
        '川菜烹饪', '粤菜烹饪', '鲁菜烹饪', '苏菜烹饪', '浙菜烹饪', '闽菜烹饪', '徽菜烹饪', '湘菜烹饪',
        '东北菜烹饪', '日本料理', '韩国料理', '西餐烹饪', '咖啡制作', '茶艺表演', '调酒技术',
        '宠物养护', '养鱼知识', '养鸟知识', '养猫知识', '养狗知识', '收藏艺术', '钱币收藏', '邮票收藏'
    ]
}


# 默认图片
DEFAULT_IMAGE = 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800'


def generate_content(title):
    return f'''{title}是一项富有魅力的活动，深受广大人民群众的喜爱。

【活动简介】
{title}是一种非常受欢迎的活动，有着悠久的历史传统和深厚的文化底蕴。经过多年的发展，这项活动已经成为现代社会生活中不可或缺的一部分。

【活动特点】
1. 参与门槛低，适合各年龄段人群参与
2. 活动形式多样，可以根据个人喜好选择不同的方式
3. 场地设施要求不高，易于开展和普及
4. 能够培养参与者的各种能力和素质

【主要益处】
- 强身健体，提高身体素质
- 培养团队协作精神和竞争意识
- 丰富业余文化生活
- 拓展社交圈子，结识志同道合的朋友
- 缓解压力，愉悦身心

【如何参与】
参与{title}活动非常简单。您可以通过以下方式加入：
1. 咨询当地的俱乐部或相关组织
2. 参加社区或单位组织的活动
3. 在线学习相关知识和技能
4. 与志同道合的朋友一起组队参与

【发展前景】
{title}的发展前景非常广阔。随着社会的进步和人民生活水平的提高，越来越多的人开始关注并积极参与这项活动。无论你是初学者还是资深爱好者，都能在这里找到属于自己的乐趣。

欢迎大家积极参与{title}，体验其中的乐趣！'''


def generate_slug(title):
    try:
        from pypinyin import lazy_pinyin
        pinyin_list = lazy_pinyin(title)
        initials = ''.join([p[0].upper() if p and len(p) > 0 else 'X' for p in pinyin_list])
        return initials[:4] or f'ACT{hash(title) % 10000}'
    except:
        return f'ACT{hash(title) % 10000}'


def populate():
    print('=' * 60)
    print('开始清空并重新填充活动百科内容（纯中文）...')
    print('=' * 60)
    
    # 清空所有现有文章
    print('\n[1] 清空现有文章...')
    deleted_count = EncyclopediaArticle.objects.all().count()
    EncyclopediaArticle.objects.all().delete()
    print(f'  [-] 已删除 {deleted_count} 篇文章')
    
    # 确保分类存在
    categories_data = {
        'sports': {'name': '体育运动类', 'icon': 'bi bi-dribbble', 'order': 1},
        'arts': {'name': '文艺表演类', 'icon': 'bi bi-music-note', 'order': 2},
        'culture': {'name': '传统文化类', 'icon': 'bi bi-book', 'order': 3},
        'academic': {'name': '学术科创类', 'icon': 'bi bi-rocket', 'order': 4},
        'public_welfare': {'name': '公益实践类', 'icon': 'bi bi-heart', 'order': 5},
        'interest': {'name': '兴趣生活类', 'icon': 'bi bi-star', 'order': 6},
    }
    
    print('\n[2] 初始化分类...')
    for slug, data in categories_data.items():
        EncyclopediaCategory.objects.get_or_create(slug=slug, defaults=data)
        print(f'  [+] {data["name"]}')
    
    # 创建文章
    print('\n[3] 创建新文章...')
    success_count = 0
    
    for cat_slug, keywords in KEYWORDS_BY_CATEGORY.items():
        category = EncyclopediaCategory.objects.get(slug=cat_slug)
        
        for keyword in keywords:
            slug = generate_slug(keyword)
            base_slug = slug
            counter = 1
            while EncyclopediaArticle.objects.filter(slug=slug).exists():
                slug = f'{base_slug}{counter}'
                counter += 1
            
            EncyclopediaArticle.objects.create(
                category=category,
                title=keyword,
                slug=slug,
                summary=f'{keyword}是一种有趣的活动，可以帮助人们丰富生活、锻炼身心。',
                content=generate_content(keyword),
                image_url=DEFAULT_IMAGE,
                source_name='智枢青寰',
                source_url='https://baike.baidu.com',
                is_published=True,
            )
            success_count += 1
            print(f'  [+] {keyword} (slug: {slug})')
    
    print('\n' + '=' * 60)
    print(f'完成！成功创建 {success_count} 篇文章（全部中文）')
    print('=' * 60)
    
    print(f'\n统计:')
    print(f'  分类总数: {EncyclopediaCategory.objects.count()}')
    print(f'  文章总数: {EncyclopediaArticle.objects.count()}')
    print(f'  有图片的文章: {EncyclopediaArticle.objects.exclude(image_url__isnull=False).exclude(image_url="").count()}')


if __name__ == '__main__':
    populate()
