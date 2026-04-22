"""
Comprehensive Encyclopedia Update Script - Expanded to 200+
"""
import os
import sys
sys.path.insert(0, r'D:\campus_club_site')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_club_site.settings')
import django
django.setup()
from clubs.models import EncyclopediaArticle, EncyclopediaCategory

# Expanded activity categories - 200+ activities
CATEGORY_MAP = {
    'sports': ['篮球', '足球', '羽毛球', '乒乓球', '网球', '排球', '游泳', '跑步', '冲浪', '武术', '体操', '跆拳道', '瑜伽', '拳击', '散打', '击剑', '马术', '射击', '射箭', '帆船', '皮划艇', '赛艇', '摩托艇', '潜水', '钓鱼', '田径', '短跑', '长跑', '马拉松', '跳高', '跳远', '铅球', '标枪', '铁饼', '撑杆跳', '三级跳', '跨栏', '竞走', '健身', '健美', '举重', '摔跤', '柔道', '空手道', '剑道', '高尔夫球', '保龄球', '台球', '壁球', '棒球', '垒球', '冰球', '雪上运动', '滑雪', '滑冰', '花样滑冰', '速度滑冰', '冰壶', '帆板', '风筝冲浪', '漂流', '溯溪', '攀岩', '野外生存', '定向运动', '徒步穿越', '公路自行车', '山地自行车', 'BMX', '卡丁车', '赛车'],
    'arts': ['舞蹈', '芭蕾舞', '现代舞', '古典舞', '民族舞', '街舞', '爵士舞', '拉丁舞', '踢踏舞', '机械舞', '嘻哈舞', '广场舞', '华尔兹', '探戈', '桑巴', '恰恰', '伦巴', '莎莎舞', '印度舞', '弗朗明哥', '歌唱', '合唱', '美声唱法', '民族唱法', '流行唱法', '摇滚', '民谣', '说唱', '音乐剧', '歌剧', '话剧', '戏剧', '戏曲', '京剧', '越剧', '豫剧', '粤剧', '川剧', '评剧', '黄梅戏', '昆曲', '相声', '小品', '快板', '评书', '曲艺', '朗诵', '演讲', '辩论', '主持', '钢琴', '小提琴', '中提琴', '大提琴', '低音提琴', '吉他', '电吉他', '贝斯', '尤克里里', '竖琴', '架子鼓', '电子鼓', '非洲鼓', '卡宏鼓', '口琴', '萨克斯', '小号', '长号', '圆号', '长笛', '短笛', '单簧管', '双簧管', '二胡', '板胡', '京胡', '高胡', '马头琴', '琵琶', '古筝', '扬琴', '笛子', '箫', '笙', '唢呐', '葫芦丝', '摄影', '摄像', '人像摄影', '风光摄影', '纪实摄影', '商业摄影', '艺术摄影', '新闻摄影', '建筑摄影', '静物摄影', '美食摄影', '宠物摄影', '婚礼摄影', '星空摄影', '延时摄影', '全景摄影', '绘画', '素描', '速写', '水彩画', '油画', '版画', '壁画', '漆画', '漫画', '连环画', '插画', '国画', '写意画', '工笔画', '书法', '篆刻', '雕塑', '陶艺', '插花', '花艺', '茶艺', '香道', '电影', '电视剧', '纪录片', '动画片', '短视频', '微电影'],
    'culture': ['剪纸', '窗花', '刻纸', '刺绣', '苏绣', '湘绣', '蜀绣', '粤绣', '编织', '竹编', '草编', '藤编', '柳编', '中国结', '风筝', '泥塑', '面塑', '糖画', '捏面人', '木偶', '皮影', '灯彩', '宫灯', '纱灯', '陶瓷', '紫砂', '漆器', '景泰蓝', '扎染', '蜡染', '围棋', '象棋', '国际象棋', '五子棋', '跳棋', '军棋', '麻将', '扑克', '桥牌', '魔方', '数独', '华容道', '九连环', '孔明锁', '脸谱'],
    'academic': ['编程', 'Python', 'Java', 'JavaScript', 'C语言', 'C++', 'C#', 'PHP', 'Ruby', 'Go语言', 'Rust', 'Swift', 'Kotlin', 'SQL', 'HTML', 'CSS', 'Vue', 'React', 'Angular', 'Node.js', 'Django', 'Flask', 'Spring', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Docker', 'Kubernetes', 'Git', 'Linux', '网络安全', 'Web安全', 'CTF', '渗透测试', '密码学', '区块链', '人工智能', '机器学习', '深度学习', '自然语言处理', '计算机视觉', '语音识别', '知识图谱', '强化学习', '云计算', '大数据', '数据分析', '数据可视化', '统计学', '算法设计', '数据结构', 'ACM', '蓝桥杯', 'LeetCode', '机器人', '工业机器人', '服务机器人', '无人机', '自动驾驶', 'Arduino', 'RaspberryPi', '3D打印', '芯片设计', '半导体', '集成电路', 'PLC', '科学实验', '物理实验', '化学实验', '生物实验', '天文观测', '天文摄影', '英语', '日语', '韩语', '法语', '德语', '西班牙语'],
    'public_welfare': ['志愿服务', '支教', '乡村支教', '社区服务', '敬老服务', '助老服务', '关爱老人', '帮困助残', '扶贫', '乡村振兴', '环保', '植树造林', '绿化', '清洁能源', '节能减排', '垃圾分类', '废物利用', '旧物捐赠', '野生动物保护', '动物救助', '动物收容', '宠物领养', '海洋保护', '湿地保护', '森林保护', '海滩清洁', '环保宣传', '应急救援', '急救培训', '心肺复苏', '止血包扎', '火灾逃生', '地震避险', '消防演练', '蓝天救援', '慈善', '募捐', '义卖', '义演', '义诊', '无偿献血', '法律援助', '心理辅导', '社区矫正'],
    'interest': ['烹饪', '烘焙', '面点', '川菜', '粤菜', '鲁菜', '苏菜', '浙菜', '闽菜', '徽菜', '湘菜', '东北菜', '日本料理', '韩国料理', '寿司', '刺身', '拉面', '咖喱', '披萨', '汉堡', '意面', '牛排', '咖啡', '茶道', '调酒', '鸡尾酒', '红酒', '饮料调制', '插花', '花艺', '茶艺', '香道', '园艺', '养花', '宠物养护', '养鱼', '养鸟', '养猫', '养狗', '仓鼠', '兔子', '爬虫', '电影', '音乐', '阅读', '文学', '小说', '诗歌', '旅行', '骑行', '登山', '滑雪', '潜水', '高尔夫', '保龄球', '台球', '棋牌', '游戏', '电竞', '动漫', '手办', '收藏', '园艺设计', '植物养护', '摄影技巧'],
}


def slugify(title):
    try:
        from pypinyin import lazy_pinyin
        pinyin_list = lazy_pinyin(title)
        initials = ''.join([p[0].upper() if p and len(p) > 0 else '' for p in pinyin_list])
        return initials[:8] if initials else f'ACT{abs(hash(title)) % 10000}'
    except:
        return f'ACT{abs(hash(title)) % 10000}'


def populate():
    print('=' * 60)
    print('Expanded Encyclopedia Population - Target: 200+')
    print('=' * 60)
    
    cats_data = {
        'sports': {'name': '体育运动类', 'icon': 'bi bi-dribbble', 'order': 1},
        'arts': {'name': '文艺表演类', 'icon': 'bi bi-music-note', 'order': 2},
        'culture': {'name': '传统文化类', 'icon': 'bi bi-book', 'order': 3},
        'academic': {'name': '学术科创类', 'icon': 'bi bi-rocket', 'order': 4},
        'public_welfare': {'name': '公益实践类', 'icon': 'bi bi-heart', 'order': 5},
        'interest': {'name': '兴趣生活类', 'icon': 'bi bi-star', 'order': 6},
    }
    
    cats = {}
    print('\n[1] Categories...')
    for slug, data in cats_data.items():
        c, _ = EncyclopediaCategory.objects.get_or_create(slug=slug, defaults=data)
        cats[slug] = c
    
    print('\n[2] Creating articles...')
    created = 0
    for cat_slug, activities in CATEGORY_MAP.items():
        cat = cats[cat_slug]
        for activity in activities:
            if EncyclopediaArticle.objects.filter(title=activity).exists():
                continue
            slug = slugify(activity)
            base_slug = slug
            n = 1
            while EncyclopediaArticle.objects.filter(slug=slug).exists():
                slug = f'{base_slug}{n}'
                n += 1
            EncyclopediaArticle.objects.create(
                category=cat, title=activity, slug=slug,
                summary=f'{activity}是一项有趣的活动，可以丰富生活、增长见识。',
                content=f'''{activity}是一项有趣的活动，深受广大人民群众的喜爱。

## 活动特点
{activity}有着自己独特的魅力和价值，适合各个年龄段的人群参与。

## 基本介绍
{activity}在社会中有着广泛的参与群体，是丰富业余生活的好选择。

## 参与价值
1. 丰富生活：增添生活乐趣
2. 社交属性：结识志同道合的朋友
3. 个人成长：提升技能和素养
4. 健康益处：有益于身心健康

## 入门建议
1. 了解基础知识
2. 循序渐进学习
3. 多参与实践活动
4. 坚持练习提高

{activity}是一个值得尝试的活动领域，欢迎大家积极参与探索。''',
                source_name='智枢青寰编辑', is_published=True
            )
            created += 1
            print(f'  + {activity}')
    
    print('\n' + '=' * 60)
    print(f'Created: {created} new articles')
    print(f'Total: {EncyclopediaArticle.objects.count()} articles')
    print('=' * 60)


if __name__ == '__main__':
    populate()
