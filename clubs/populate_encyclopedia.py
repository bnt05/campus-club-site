"""
填充活动百科内容（使用预设内容）
由于百度百科有反爬机制，此脚本使用预设内容填充百科
"""
import os
import sys

# Setup Django
sys.path.insert(0, r'D:\campus_club_site')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_club_site.settings')
import django
django.setup()

from clubs.models import EncyclopediaCategory, EncyclopediaArticle


# 预设百科内容
CATEGORIES = {
    'sports': {'name': '体育竞技类', 'icon': 'bi bi-dribbble', 'order': 1},
    'arts': {'name': '文艺表演类', 'icon': 'bi bi-music-note', 'order': 2},
    'culture': {'name': '传统文化类', 'icon': 'bi bi-book', 'order': 3},
    'academic': {'name': '学术科创类', 'icon': 'bi bi-rocket', 'order': 4},
    'public_welfare': {'name': '公益实践类', 'icon': 'bi bi-heart', 'order': 5},
    'interest': {'name': '兴趣生活类', 'icon': 'bi bi-star', 'order': 6},
}

ARTICLES = [
    # 体育类
    {'category': 'sports', 'title': '篮球', 'summary': '篮球是以手为中心的身体对抗性运动，是奥运会核心比赛项目。', 'content': '篮球(Basketball)是一项以手为中心的对抗性体育运动，起源于美国马萨诸塞州，由基督教青年会学校教师詹姆斯·奈史密斯于1891年发明。\n\n历史起源：篮球运动起源于美国马萨诸塞州斯普林菲尔德的基督教青年会国际训练学校，由体育教师詹姆斯·奈史密斯于1891年发明。\n\n主要规则：每队5名球员在场，比赛分4节，每节10-12分钟，将球投入对方篮筐得2-3分。\n\n主要赛事：NBA（美国职业篮球联赛）、CBA（中国男子篮球职业联赛）、奥运会篮球比赛。\n\n健康益处：篮球运动可以增强心肺功能，提高身体协调性，培养团队合作精神。', 'is_featured': True},
    {'category': 'sports', 'title': '足球', 'summary': '足球是以脚为主支配球的体育运动，被誉为世界第一运动。', 'content': '足球(Football)是一项以脚为主支配球的体育运动，是全球体育界最具影响力的单项体育运动，被誉为"世界第一运动"。\n\n历史起源：足球运动的历史可以追溯到古代，中国古代的蹴鞠被认为是足球运动的最早形式，现代足球起源于英国。\n\n主要规则：每队11名球员，比赛分两个45分钟半场，将球踢入对方球门得1分。\n\n主要赛事：FIFA世界杯、欧洲冠军联赛、中国足球协会超级联赛。\n\n健康益处：足球运动能增强体质，提高心肺功能，培养团队意识和顽强拼搏的精神。', 'is_featured': True},
    {'category': 'sports', 'title': '羽毛球', 'summary': '羽毛球是隔着球网，使用球拍将球击打过网的对抗性运动。', 'content': '羽毛球(Badminton)是一项隔着球网，使用球拍将球击打过网的对抗性运动。\n\n历史起源：羽毛球运动的起源可以追溯到古代日本和中国的游戏，现代羽毛球运动于1873年在英国诞生。\n\n主要规则：单打和双打两种形式，比赛采用21分制，三局两胜。\n\n主要赛事：奥运会羽毛球比赛、世界羽毛球锦标赛、全英羽毛球公开赛。\n\n健康益处：羽毛球运动可以锻炼全身肌肉，增强心肺功能，提高反应速度和协调性。', 'is_featured': False},
    {'category': 'sports', 'title': '乒乓球', 'summary': '乒乓球是以球拍击球的小球运动，素有"国球"之称。', 'content': '乒乓球(Table Tennis)是一项以球拍击球的小球运动，因其打击时发出"乒乒乓乓"的声音而得名，在中国有"国球"之称。\n\n历史起源：乒乓球运动起源于19世纪末的英国，最初是一种餐桌网球，后来逐渐演变成现在的形式。\n\n主要规则：单打和双打两种形式，比赛采用11分制，五局三胜或七局四胜。\n\n主要赛事：世界乒乓球锦标赛、奥运会乒乓球比赛、WTT世界乒联巡回赛。\n\n健康益处：乒乓球运动可以锻炼眼部肌肉，改善视力，提高反应速度和手眼协调能力。', 'is_featured': False},
    {'category': 'sports', 'title': '游泳', 'summary': '游泳是在水中进行的人类活动，是人类与生俱来的本能之一。', 'content': '游泳(Swimming)是在水中进行的人类活动，是人类与生俱来的本能之一。游泳可以锻炼全身肌肉，提高心肺功能。\n\n历史起源：人类在史前时代就学会了游泳，古代埃及、希腊、罗马等文明都有游泳的记录，现代竞技游泳在19世纪开始发展。\n\n主要泳姿：自由泳（爬泳）、仰泳、蛙泳、蝶泳。\n\n主要赛事：奥运会游泳比赛、世界游泳锦标赛。\n\n健康益处：游泳可以增强心肺功能，锻炼全身肌肉，减轻关节压力。', 'is_featured': False},
    # 文艺类
    {'category': 'arts', 'title': '书法', 'summary': '书法是中国传统文化艺术，通过毛笔书写汉字的艺术。', 'content': '书法(Calligraphy)是中国传统文化艺术，是书写汉字的艺术。书法不仅是写字的技术，更是中华文化的重要载体。\n\n历史起源：书法艺术起源于汉字的发明，甲骨文是中国已知最早的书法作品。经历了篆书、隶书、楷书、行书、草书等发展阶段。\n\n主要书体：篆书（圆转流畅）、隶书（横平竖直）、楷书（规矩端正）、行书（流畅灵动）、草书（笔走龙蛇）。\n\n代表人物：王羲之（书圣）、颜真卿、柳公权、苏轼。\n\n健康益处：学习书法可以修身养性，培养耐心和专注力，对身心健康都有益处。', 'is_featured': True},
    {'category': 'arts', 'title': '绘画', 'summary': '绘画是运用线条、色彩、构图等艺术语言，创造视觉形象的艺术。', 'content': '绘画(Painting)是运用线条、色彩、构图等艺术语言，在平面上创造视觉形象的艺术形式。\n\n主要画种：中国画（包括写意和工笔）、油画、水彩画、版画、素描。\n\n主要流派：写实派、抽象派、印象派、现代派。\n\n代表人物：达·芬奇、毕加索、张择端、徐悲鸿。\n\n健康益处：绘画可以培养创造力和审美能力，帮助表达情感，对心理健康有益。', 'is_featured': False},
    {'category': 'arts', 'title': '舞蹈', 'summary': '舞蹈是以人体动作为主要表现手段的时空艺术。', 'content': '舞蹈(Dance)是以人体动作为主要表现手段的时空艺术，通过有节奏的动作和姿态来表达情感。\n\n主要舞种：中国舞、芭蕾、现代舞、街舞、拉丁舞。\n\n主要赛事：桃李杯舞蹈比赛、CCTV电视舞蹈大赛、国际舞蹈比赛。\n\n健康益处：舞蹈可以增强身体协调性，塑造优美体态，提高音乐素养，培养自信心。', 'is_featured': False},
    {'category': 'arts', 'title': '歌唱', 'summary': '歌唱是人声与音乐结合的艺术表现形式。', 'content': '歌唱(Singing)是人声与音乐结合的艺术表现形式，是人类最本能的音乐表达方式。\n\n声乐类型：美声唱法、民族唱法、流行唱法、通俗唱法。\n\n主要赛事：中国好声音、超级女声/超级男声、歌手大赛。\n\n健康益处：歌唱可以锻炼肺活量，调节情绪，释放压力，对心理健康有益。', 'is_featured': False},
    # 文化类
    {'category': 'culture', 'title': '剪纸', 'summary': '剪纸是中国传统民间艺术，以纸为材料剪出各种图案。', 'content': '剪纸(Paper Cutting)是中国传统民间艺术，是以纸为材料，用剪刀或刻刀剪出各种图案的艺术形式。\n\n历史起源：剪纸艺术起源于汉代，至今已有1500多年的历史。2009年，中国剪纸入选联合国教科文组织人类非物质文化遗产代表作名录。\n\n主要技法：阴刻（剪去图案部分）、阳刻（保留图案部分）、阴阳刻结合。\n\n健康益处：剪纸可以培养耐心和精细动作能力，传承传统文化，丰富精神生活。', 'is_featured': True},
    {'category': 'culture', 'title': '茶道', 'summary': '茶道是通过泡茶、饮茶来修身养性的生活艺术。', 'content': '茶道(Tea Ceremony)是通过泡茶、饮茶来修身养性的生活艺术，体现了东方文化的精髓。\n\n历史起源：茶道起源于中国，唐代陆羽所著《茶经》是中国茶道的开创之作。后来传播到日本，发展成为日本茶道。\n\n基本流程：备器、煮水、温杯、投茶、注水、奉茶、饮茶。\n\n健康益处：茶道可以静心养性，增进友谊，提高生活品质。', 'is_featured': False},
    {'category': 'culture', 'title': '围棋', 'summary': '围棋是一种策略性棋类游戏，起源于中国。', 'content': '围棋(Go/Weiqi)是一种策略性棋类游戏，起源于中国，距今已有4000多年历史。\n\n历史起源：围棋起源于中国，相传为尧舜所造。隋唐时期传入日本，后传播到世界各地。\n\n基本规则：棋盘19×19格，黑子先手，围住对方棋子即可吃子。\n\n主要赛事：应氏杯世界围棋锦标赛、春兰杯世界职业围棋锦标赛。\n\n健康益处：围棋可以锻炼逻辑思维，培养耐心和专注力，预防老年痴呆。', 'is_featured': False},
    # 学术类
    {'category': 'academic', 'title': '编程', 'summary': '编程是让计算机执行特定任务的技术过程。', 'content': '编程(Programming)是让计算机执行特定任务的技术过程，是现代科技发展的基础。\n\n主要编程语言：Python（简单易学）、Java（企业级应用）、JavaScript（网页开发）、C/C++（系统编程）。\n\n应用领域：Web开发、移动开发、数据科学、游戏开发、嵌入式开发。\n\n主要赛事：ACM国际大学生程序设计竞赛、蓝桥杯程序设计大赛。\n\n健康益处：编程可以锻炼逻辑思维和解决问题的能力，是未来必备技能。', 'is_featured': True},
    {'category': 'academic', 'title': '机器人', 'summary': '机器人是能够自动执行任务的机械装置。', 'content': '机器人(Robot)是能够自动执行任务的机械装置，是人工智能的重要载体。\n\n发展历史：1920年，捷克作家卡雷尔·恰佩克在戏剧中首次使用"robot"一词。\n\n主要类型：工业机器人、服务机器人、特种机器人、人形机器人。\n\n技术组成：机械结构、传感器、执行器、控制系统。\n\n主要赛事：ROBOCON全国大学生机器人大赛、中国机器人大赛。\n\n健康益处：学习机器人技术可以培养创新思维和动手能力。', 'is_featured': False},
    {'category': 'academic', 'title': '科学实验', 'summary': '科学实验是验证科学假设、探索自然规律的重要方法。', 'content': '科学实验(Scientific Experiment)是验证科学假设、探索自然规律的重要方法。\n\n基本步骤：观察（发现现象）、假设（提出猜想）、实验（验证假设）、分析（处理数据）、结论（得出结果）。\n\n常见实验类型：物理实验（力、热，光、电）、化学实验（物质变化）、生物实验（生命现象）。\n\n安全注意事项：遵守实验室规则、正确使用仪器、了解化学品性质。\n\n健康益处：科学实验可以培养科学思维和探索精神，提高动手能力。', 'is_featured': False},
    # 公益类
    {'category': 'public_welfare', 'title': '志愿服务', 'summary': '志愿服务是不以获得报酬为目的，自愿贡献时间和精力。', 'content': '志愿服务(Volunteer Service)是不以获得物质报酬为目的，自愿贡献个人的时间和精力，为社会提供服务和帮助的行为。\n\n主要领域：社区服务、环保志愿、支教服务、助老服务、大型赛会。\n\n主要组织：中国志愿服务联合会、各高校志愿者协会、社会公益组织。\n\n参与方式：加入志愿者组织、参加志愿服务活动、宣传志愿服务精神。\n\n健康益处：参与志愿服务可以提升社会责任感，实现自我价值，收获友谊和快乐。', 'is_featured': True},
    {'category': 'public_welfare', 'title': '环保行动', 'summary': '环保行动是为保护环境、节约资源而采取的行动。', 'content': '环保行动(Environmental Protection)是为保护环境、节约资源而采取的各种行动。\n\n主要内容：节能减排（减少能源消耗）、垃圾分类（将垃圾按类投放）、植树造林（增加绿色覆盖）。\n\n参与方式：日常生活践行环保理念、参加环保宣传活动、参与植树造林活动。\n\n环保纪念日：世界环境日（6月5日）、地球日（4月22日）、植树节（3月12日）。\n\n健康益处：环保行动可以改善生活环境，促进可持续发展。', 'is_featured': False},
    # 兴趣类
    {'category': 'interest', 'title': '摄影', 'summary': '摄影是通过光学仪器记录影像的艺术和技术。', 'content': '摄影(Photography)是通过光学仪器记录影像的艺术和技术，是一种将瞬间变为永恒的艺术形式。\n\n主要类型：风光摄影、人像摄影、纪实摄影、商业摄影、艺术摄影。\n\n基本要素：光线（摄影的灵魂）、构图（画面的布局）、色彩（视觉的感受）、时机（决定性瞬间）。\n\n主要赛事：平遥国际摄影大展、中国摄影艺术展、PSA国际摄影展。\n\n健康益处：摄影可以培养发现美的眼光，丰富精神生活，留下珍贵回忆。', 'is_featured': False},
    {'category': 'interest', 'title': '魔方', 'summary': '魔方是一种益智玩具，可以锻炼手眼协调能力。', 'content': '魔方(Rubiks Cube)是一种益智玩具，通过旋转使每个面都变成相同颜色。\n\n历史起源：魔方由匈牙利建筑学教授鲁比克·艾尔内于1974年发明，最初是为了帮助学生理解空间概念。\n\n主要类型：二阶魔方（2×2×2）、三阶魔方（3×3×3，最常见）、四阶魔方、五阶魔方。\n\n还原方法：层先法（适合初学者）、CFOP法（进阶方法）、盲拧法。\n\n主要赛事：世界魔方锦标赛、亚洲魔方锦标赛、中国魔方公开赛。\n\n健康益处：魔方可以锻炼空间想象力和手眼协调能力，培养耐心和专注力。', 'is_featured': False},
    {'category': 'interest', 'title': '乐器演奏', 'summary': '乐器演奏是通过乐器演奏音乐的艺术活动。', 'content': '乐器演奏(Musical Performance)是通过乐器演奏音乐的艺术活动，是人类表达情感的重要方式之一。\n\n乐器分类：弦乐（钢琴、小提琴、吉他、古筝）、管乐（长笛、萨克斯、笛子）、打击乐（架子鼓）、民乐（二胡、琵琶、扬琴）。\n\n学习途径：学校音乐课、少年宫培训、私人教师、在线学习。\n\n主要赛事：肖邦国际钢琴比赛、中国音乐金钟奖、各器乐考级。\n\n健康益处：学习乐器可以提高音乐素养，培养专注力和记忆力，丰富精神生活。', 'is_featured': False},
]


def generate_slug(title):
    """生成slug"""
    try:
        from pypinyin import lazy_pinyin
        pinyin_list = lazy_pinyin(title)
        initials = ''.join([p[0].upper() if p and len(p) > 0 else 'X' for p in pinyin_list])
        slug = initials[:4]
        if not slug or len(slug) < 2:
            slug = f'ART{hash(title) % 10000}'
        return slug
    except:
        return f'ART{hash(title) % 10000}'


def populate_encyclopedia():
    """填充百科内容"""
    print('=' * 50)
    print('Start populating encyclopedia...')
    print('=' * 50)
    
    # Create categories
    print('\n[1] Creating categories...')
    for slug, data in CATEGORIES.items():
        category, created = EncyclopediaCategory.objects.get_or_create(
            slug=slug,
            defaults=data
        )
        print(f'  [+] Category: {data["name"]}')
    
    # Create articles
    print('\n[2] Creating articles...')
    success_count = 0
    for article_data in ARTICLES:
        title = article_data['title']
        
        # Check if already exists
        if EncyclopediaArticle.objects.filter(title=title).exists():
            print(f'  [=] Article exists: {title}')
            continue
        
        category_slug = article_data.pop('category')
        category = EncyclopediaCategory.objects.get(slug=category_slug)
        
        # Generate slug
        slug = generate_slug(title)
        # Ensure unique slug
        base_slug = slug
        counter = 1
        while EncyclopediaArticle.objects.filter(slug=slug).exists():
            slug = f'{base_slug}{counter}'
            counter += 1
        
        # Create article
        article = EncyclopediaArticle.objects.create(
            category=category,
            title=title,
            slug=slug,
            summary=article_data['summary'],
            content=article_data['content'],
            source_name='Zhishu Qinghuan',
            is_featured=article_data.get('is_featured', False),
            is_published=True,
        )
        print(f'  [+] Article: {article.title} (slug: {slug})')
        success_count += 1
    
    print('\n' + '=' * 50)
    print(f'Done! Created {success_count} articles')
    print('=' * 50)
    
    # Print stats
    print(f'\nStats:')
    print(f'  Categories: {EncyclopediaCategory.objects.count()}')
    print(f'  Articles: {EncyclopediaArticle.objects.count()}')
    print(f'  Featured: {EncyclopediaArticle.objects.filter(is_featured=True).count()}')


if __name__ == '__main__':
    populate_encyclopedia()
