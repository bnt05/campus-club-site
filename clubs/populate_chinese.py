"""
重新生成百科内容 - 纯中文关键词
"""
import os
import sys
import time

sys.path.insert(0, r'D:\campus_club_site')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_club_site.settings')
import django
django.setup()

from clubs.models import EncyclopediaCategory, EncyclopediaArticle


# 纯中文关键词列表 - 300+活动
ACTIVITY_KEYWORDS = [
    # 体育运动类
    '篮球', '足球', '羽毛球', '乒乓球', '网球', '排球', '沙滩排球', '高尔夫球', '保龄球', '台球', '壁球', '曲棍球', '棒球', '垒球', '冰球', '滑雪', '滑冰', '花样滑冰', '速度滑冰', '短道速滑', '冰壶', '雪橇', '游泳', '跳水', '水球', '帆船', '帆板', '皮划艇', '赛艇', '冲浪', '潜水', '钓鱼', '田径', '短跑', '中长跑', '长跑', '马拉松', '跨栏', '跳高', '跳远', '三级跳远', '撑杆跳', '铅球', '铁饼', '标枪', '体操', '艺术体操', '蹦床', '健美操', '街舞', '跆拳道', '武术', '散打', '太极拳', '拳击', '击剑', '马术', '登山', '攀岩', '野外生存', '定向运动', '徒步', '骑行', '拓展训练',
    
    # 文艺表演类
    '歌唱', '合唱', '美声', '民族唱法', '流行唱法', '摇滚', '民谣', '说唱', '音乐剧', '歌剧', '话剧', '戏剧', '京剧', '越剧', '黄梅戏', '豫剧', '粤剧', '川剧', '评剧', '小品', '相声', '杂技', '魔术', '舞蹈', '芭蕾舞', '现代舞', '古典舞', '民族舞', '爵士舞', '拉丁舞', '桑巴舞', '恰恰舞', '伦巴舞', '斗牛舞', '瑜伽',
    
    # 传统文化类
    '书法', '楷书', '行书', '草书', '隶书', '篆书', '国画', '写意画', '工笔画', '人物画', '山水画', '花鸟画', '素描', '水彩画', '油画', '版画', '壁画', '剪纸', '窗花', '刺绣', '编织', '竹编', '草编', '中国结', '风筝', '泥塑', '面塑', '木偶', '皮影', '陶瓷', '紫砂', '青瓷', '茶道', '茶艺', '围棋', '象棋', '国际象棋', '五子棋', '麻将', '扑克牌', '魔方', '香道', '插花', '花艺',
    
    # 学术科创类
    '编程', '机器人', '人工智能', '机器学习', '深度学习', '大数据', '云计算', '网络安全', 'Web开发', '数据库', '算法设计', '数据结构', '电子制作', '3D打印', '航空航天', '天文观测', '天文摄影', '科学实验', '物理实验', '化学实验', '生物实验', '地理考察', '气象观测', '地震监测', '矿石标本', '植物学', '动物学', '微生物学', '化学工程', '材料科学', '纳米技术', '生物工程', '基因工程', '环境保护', '新能源技术', '核能技术', '太阳能技术', '风能技术', '地热能技术', '海洋技术', '测绘技术', '遥感技术', '北斗导航', '物联网技术', '区块链技术', '虚拟现实', '增强现实', '无人机技术', '自动驾驶技术', '芯片技术', '半导体技术',
    
    # 公益实践类
    '志愿服务', '公益活动', '慈善捐赠', '义演义卖', '支教活动', '社区服务', '敬老服务', '助残服务', '扶贫活动', '环保行动', '植树造林', '垃圾分类', '野生动物保护', '动物救助', '海洋保护', '湿地保护', '森林保护', '河流保护', '应急救援', '急救培训', '消防演练', '心理援助', '无偿献血', '骨髓捐献', '器官捐献', '关爱留守儿童', '关爱空巢老人', '关爱农民工', '关爱贫困学生', '法律援助', '科普宣传', '文化下乡', '卫生下乡', '科技下乡',
    
    # 兴趣生活类
    '摄影', '人像摄影', '风光摄影', '纪实摄影', '微距摄影', '天文摄影', '建筑摄影', '美食摄影', '宠物摄影', '婚礼摄影', '电影', '电视剧', '纪录片', '动画片', '短视频', 'Vlog制作', '阅读', '文学创作', '诗歌创作', '小说写作', '散文写作', '钢琴', '小提琴', '吉他', '架子鼓', '二胡', '琵琶', '古筝', '笛子', '萨克斯', '手风琴', '口琴', '烹饪', '烘焙', '面点制作', '川菜', '粤菜', '鲁菜', '苏菜', '浙菜', '闽菜', '徽菜', '湘菜', '东北菜', '日本料理', '韩国料理', '西餐', '咖啡制作', '茶艺表演', '调酒', '插花艺术', '园艺设计', '宠物养护', '养鱼', '养鸟', '养猫', '养狗', '收藏', '钱币收藏', '邮票收藏', '古玩收藏', '书画收藏', '根雕', '奇石', '盆景', '园艺', '园林设计', '旅行', '自驾游', '露营', '徒步旅行', '骑行旅行', '潜水', '冲浪', '滑雪', '高尔夫', '马术', '帆船', '游艇', '赛车', '卡丁车', '摩托车', '自行车', '滑板', '轮滑', '保龄球', '台球', '高尔夫球练习', '门球', '板球', '橄榄球', '曲棍球', '地板球', '壁球', '羽毛球', '乒乓球', '网球', '排球', '篮球', '足球', '手球', '水球', '沙排', '毽球', '板球', '棒球', '垒球', '冰球', '雪球', '雪地摩托', '狗拉雪橇', '滑草', '滑沙', '卡丁车', '赛车', '拉力赛', '越野赛', '登山', '攀岩', '攀冰', '速降', '蹦极', '跳伞', '滑翔伞', '热气球', '飞行执照', '航海', '划船', '皮划艇', '帆船', '冲浪', '潜水', '浮潜', '水肺潜水', '自由潜水', '花样游泳', '花样滑冰', '速度滑冰', '短道速滑', '冰壶', '冰球', '雪橇', '有舵雪橇', '无舵雪橇', '俯式冰橇', '跳台滑雪', '越野滑雪', '单板滑雪', '双板滑雪', '自由式滑雪', '追逐赛', '半管赛', '障碍赛', 'U型池', '街式赛', '公园赛', '速降赛', '耐力赛', '山地赛', ' XC赛', 'DH赛', 'FR赛', 'DJ赛', 'SS赛', 'CCR赛', 'CMS赛', 'Enduro赛', 'Trial赛', 'Trials赛', '双人越野', '四人越野'
]


# 预设图片URL - 用于没有爬取到图片时使用
# 这些是免费的Unsplash图片链接
IMAGE_URLS = {
    '篮球': 'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=800',
    '足球': 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=800',
    '羽毛球': 'https://images.unsplash.com/photo-1599256621730-0fd2443623ed?w=800',
    '乒乓球': 'https://images.unsplash.com/photo-1534158914592-062992fbe609?w=800',
    '网球': 'https://images.unsplash.com/photo-1554068865-24cecd4e54b8?w=800',
    '排球': 'https://images.unsplash.com/photo-1612872087720-bb876e2e4d14?w=800',
    '游泳': 'https://images.unsplash.com/photo-1560090995-01632a28895b?w=800',
    '田径': 'https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=800',
    '马拉松': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',
    '体操': 'https://images.unsplash.com/photo-1526232761682-d26e03ac148e?w=800',
    '武术': 'https://images.unsplash.com/photo-1544367567-0f2fe5c0d5c6?w=800',
    '跆拳道': 'https://images.unsplash.com/photo-1555597673-b411d2dd7f0a?w=800',
    '拳击': 'https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?w=800',
    '瑜伽': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800',
    '骑行': 'https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=800',
    '登山': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800',
    '攀岩': 'https://images.unsplash.com/photo-1522163182402-834f871fd851?w=800',
    '歌唱': 'https://images.unsplash.com/photo-1516280440614-37939bbacd81?w=800',
    '舞蹈': 'https://images.unsplash.com/photo-1508700929628-666bc8bd84ea?w=800',
    '芭蕾舞': 'https://images.unsplash.com/photo-1518834107812-67b0b7c5843e?w=800',
    '书法': 'https://images.unsplash.com/photo-1517971129774-8a2d38d3e37d?w=800',
    '绘画': 'https://images.unsplash.com/photo-1513364776144-60967b0f7f83?w=800',
    '剪纸': 'https://images.unsplash.com/photo-1604431698585-e379a78a8d0c?w=800',
    '摄影': 'https://images.unsplash.com/photo-1452587925148-ce544e77e70d?w=800',
    '烹饪': 'https://images.unsplash.com/photo-1556910103-1c02745aae4d?w=800',
    '烘焙': 'https://images.unsplash.com/photo-1486427944299-d1955d23e34d?w=800',
    '咖啡': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=800',
    '茶道': 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=800',
    '围棋': 'https://images.unsplash.com/photo-1529699211952-734e80c4d18b?w=800',
    '象棋': 'https://images.unsplash.com/photo-1529699211952-734e80c4d18b?w=800',
    '魔方': 'https://images.unsplash.com/photo-1552527806-33776ac54e76?w=800',
    '机器人': 'https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800',
    '人工智能': 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800',
    '编程': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800',
    '科学实验': 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=800',
    '天文': 'https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=800',
    '环保': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800',
    '志愿服务': 'https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=800',
}


def get_image_url(title):
    """获取图片URL"""
    # 精确匹配
    if title in IMAGE_URLS:
        return IMAGE_URLS[title]
    # 模糊匹配
    for key, url in IMAGE_URLS.items():
        if key in title or title in key:
            return url
    # 默认图片
    return 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800'


def generate_content(title):
    """生成文章内容"""
    content = f'''{title}是一项富有魅力的活动，深受广大人民群众的喜爱。

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


def populate():
    """填充百科内容"""
    print('=' * 50)
    print('开始填充活动百科内容（纯中文）...')
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
    
    print('\n[1] 初始化分类...')
    for slug, data in categories_data.items():
        category, created = EncyclopediaCategory.objects.get_or_create(
            slug=slug,
            defaults=data
        )
        print(f'  [+] {data["name"]}')
    
    # 分配关键词到分类
    keywords_by_category = {
        'sports': ACTIVITY_KEYWORDS[:65],
        'arts': ACTIVITY_KEYWORDS[65:130],
        'culture': ACTIVITY_KEYWORDS[130:195],
        'academic': ACTIVITY_KEYWORDS[195:260],
        'public_welfare': ACTIVITY_KEYWORDS[260:325],
        'interest': ACTIVITY_KEYWORDS[325:],
    }
    
    print('\n[2] 创建文章...')
    success_count = 0
    skip_count = 0
    
    for cat_slug, keywords in keywords_by_category.items():
        category = EncyclopediaCategory.objects.get(slug=cat_slug)
        
        for keyword in keywords:
            if EncyclopediaArticle.objects.filter(title=keyword).exists():
                skip_count += 1
                continue
            
            slug = generate_slug(keyword)
            base_slug = slug
            counter = 1
            while EncyclopediaArticle.objects.filter(slug=slug).exists():
                slug = f'{base_slug}{counter}'
                counter += 1
            
            content = generate_content(keyword)
            summary = f'{keyword}是一种有趣的活动，可以帮助人们丰富生活、锻炼身心。'
            image_url = get_image_url(keyword)
            
            article = EncyclopediaArticle.objects.create(
                category=category,
                title=keyword,
                slug=slug,
                summary=summary,
                content=content,
                image_url=image_url,
                source_name='智枢青寰编辑',
                source_url='https://baike.baidu.com',
                is_published=True,
            )
            print(f'  [+] {keyword} (slug: {slug})')
            success_count += 1
            time.sleep(0.05)
    
    print('\n' + '=' * 50)
    print(f'完成！成功创建 {success_count} 篇文章，跳过 {skip_count} 篇（已存在）')
    print('=' * 50)
    
    print(f'\n统计:')
    print(f'  分类总数: {EncyclopediaCategory.objects.count()}')
    print(f'  文章总数: {EncyclopediaArticle.objects.count()}')
    print(f'  有图片的文章: {EncyclopediaArticle.objects.exclude(image_url='').count()}')


if __name__ == '__main__':
    populate()
