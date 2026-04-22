"""
Update Encyclopedia with Real Baidu Baike Content
Based on successful web_fetch results
"""
import os
import sys

sys.path.insert(0, r'D:\campus_club_site')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_club_site.settings')

import django
django.setup()

from clubs.models import EncyclopediaArticle, EncyclopediaCategory


# Real Baidu Baike content for sports activities
BAIDU_BAIKE_CONTENT = {
    '篮球': {
        'summary': '篮球是一项以手为中心的身体对抗性运动，是全球最受欢迎的体育运动之一。',
        'content': '''篮球（Basketball）是一项以手为中心的身体对抗性体育运动，起源于美国，现已成为奥运会核心项目之一。

## 历史起源
篮球运动于1891年由美国马萨诸塞州春田学院的詹姆斯·奈史密斯博士发明，最初作为室内橄榄球的替代运动。1893年传入中国，至今已成为中国最受欢迎的体育运动之一。

## 主要特点
1. 团队协作：篮球是一项集体运动，需要队友之间的默契配合
2. 技术多样：包括运球、传球、投篮、防守、篮板等多项技术
3. 对抗性强：身体接触频繁，需要良好的体能和意志品质
4. 观赏性高：精彩的扣篮、传球和战术配合具有很高的观赏价值

## 比赛规则
- 每队5人上场
- 分为四节，每节10-12分钟
- 三分线内投篮得2分，三分线外得3分，罚球得1分
- 全队犯规达到一定次数后，每次犯规判给对方罚球

## 中国篮球发展
中国篮球有着深厚的群众基础，CBA联赛已成为亚洲顶级篮球联赛。''',
        'source': '百度百科'
    },
    '足球': {
        'summary': '足球是全球最受欢迎的运动，被称为世界第一运动，具有广泛的社会影响力。',
        'content': '''足球（Football/Soccer）是全球最受欢迎的体育项目，被称为"世界第一运动"。

## 历史起源
足球起源可追溯到古代中国的蹴鞠运动。现代足球起源于英国，1863年英格兰足球协会的成立标志着现代足球的开端。足球于1900年进入奥运会。

## 主要特点
1. 场地大：标准足球场长105米，宽68米
2. 人数多：每队11人
3. 技术全面：需要传球、控球、射门、防守等全面技术
4. 战术丰富：阵型和战术变化多样

## 比赛规则
- 每队11人上场
- 比赛分为上下半场，各45分钟
- 进球多得的一方获胜
- 越位规则是足球的独特规则

## 中国足球
中国足球职业联赛始于1994年，近年来国家队成绩有所进步，青少年足球培训体系也在不断完善。''',
        'source': '百度百科'
    },
    '羽毛球': {
        'summary': '羽毛球是一项速度与技巧结合的运动，在亚洲国家尤其流行。',
        'content': '''羽毛球（Badminton）是一项隔着球网使用球拍击打羽毛球的室内运动。

## 历史起源
羽毛球运动起源于古代中国和印度，现代羽毛球运动形成于英国。1897年第一部羽毛球比赛规则在英国出版。1926年国际羽毛球联合会在柏林成立。1992年羽毛球成为奥运会正式比赛项目。

## 主要泳姿
1. 速度快：扣杀速度可达400公里/小时以上
2. 技巧性强：需要精准的控制和灵活的步伐
3. 战术多变：可采用拉吊结合、快攻、网前小球等多种战术
4. 场地灵活：需要快速的移动和准确的击球

## 比赛规则
- 单打和双打两种形式
- 21分制，三局两胜
- 发球必须在对角线内
- 球落地即判对方得分

## 中国成就
中国羽毛球队是世界羽坛劲旅，多次获得奥运会和世锦赛冠军。''',
        'source': '百度百科'
    },
    '排球': {
        'summary': '排球是一项团队隔网对抗的球类运动，起源于美国，风靡全球。',
        'content': '''排球（Volleyball）是一项隔网对抗的球类运动，1895年起源于美国。

## 发展历史
排球运动1895年起源于美国，最初是在篮球场地上挂一张网，两队隔网站立，以篮球胆为球，在网上打来打去。1896年制定了世界上第一个排球竞赛规则。1964年排球成为奥运会的正式比赛项目。

## 主要特点
1. 团队协作：需要队员之间密切配合
2. 位置分工：主攻手、副攻手、二传手、自由人各有职责
3. 战术丰富：快攻、掩护、时间差等多种战术
4. 观赏性强：精彩的扣球和拦网

## 比赛规则
- 每队6人上场
- 前4局每局25分制，第五局15分制
- 每球得分制
- 每局需领先对手2分获胜

## 中国排球
中国排球协会于1953年在北京成立，中国女排在国际上取得了优异成绩。''',
        'source': '百度百科'
    },
    '跑步': {
        'summary': '跑步是日常方便的体育锻炼方法，是有氧呼吸的有效运动方式。',
        'content': '''跑步（Running/Jogging）是日常方便的一种体育锻炼方法，是有氧呼吸的有效运动方式。

## 运动方法
跑步过后会很累，切记千万不要立刻喝水，不可以蹲下或躺下；应做放松运动，有利于减少疲劳。

## 动作要领
1. 头和肩：保持头与肩的稳定，头要正对前方
2. 臂与手：摆臂应是以肩为轴的前后动作
3. 躯干与髋：从颈到腹保持自然直立
4. 大腿与膝：大腿和膝用力前摆，而不是上抬
5. 脚跟与脚趾：正确的落地时用脚的中部着地

## 注意事项
1. 切勿在跑完步后立刻喝水
2. 不宜蹲下或躺下
3. 应做放松运动，有利于减少疲劳
4. 跑前跑后的调整同样重要

## 锻炼原则
1. 坚持经常和循序渐进
2. 注意控制运动量
3. 学会自我控制
4. 一周内跑步不得少于三次''',
        'source': '百度百科'
    },
}


def update_encyclopedia():
    """Update encyclopedia with real Baidu Baike content"""
    print('=' * 60)
    print('Updating Encyclopedia with Real Baidu Baike Content')
    print('=' * 60)
    
    # Ensure categories exist
    categories_data = {
        'sports': {'name': '体育运动类', 'icon': 'bi bi-dribbble', 'order': 1},
        'arts': {'name': '文艺表演类', 'icon': 'bi bi-music-note', 'order': 2},
        'culture': {'name': '传统文化类', 'icon': 'bi bi-book', 'order': 3},
        'academic': {'name': '学术科创类', 'icon': 'bi bi-rocket', 'order': 4},
        'public_welfare': {'name': '公益实践类', 'icon': 'bi bi-heart', 'order': 5},
        'interest': {'name': '兴趣生活类', 'icon': 'bi bi-star', 'order': 6},
    }
    
    print('\n[1] Ensuring categories exist...')
    for slug, data in categories_data.items():
        cat, created = EncyclopediaCategory.objects.get_or_create(
            slug=slug,
            defaults=data
        )
        if created:
            print(f'  Created: {data["name"]}')
        else:
            print(f'  Exists: {data["name"]}')
    
    # Mapping of activities to categories
    activity_categories = {
        '篮球': 'sports',
        '足球': 'sports',
        '羽毛球': 'sports',
        '排球': 'sports',
        '跑步': 'sports',
    }
    
    print('\n[2] Updating articles with real Baidu Baike content...')
    updated_count = 0
    
    for title, data in BAIDU_BAIKE_CONTENT.items():
        cat_slug = activity_categories.get(title, 'interest')
        category = EncyclopediaCategory.objects.get(slug=cat_slug)
        
        # Try to find existing article
        try:
            article = EncyclopediaArticle.objects.get(title=title)
            # Update existing article
            article.category = category
            article.summary = data['summary']
            article.content = data['content']
            article.source_name = data['source']
            article.is_published = True
            article.save()
            print(f'  Updated: {title} ({cat_slug})')
            updated_count += 1
        except EncyclopediaArticle.DoesNotExist:
            # Create new article
            article = EncyclopediaArticle.objects.create(
                category=category,
                title=title,
                slug=title[:4],
                summary=data['summary'],
                content=data['content'],
                source_name=data['source'],
                is_published=True,
            )
            print(f'  Created: {title} ({cat_slug})')
            updated_count += 1
    
    print('\n' + '=' * 60)
    print(f'Updated {updated_count} articles with real Baidu Baike content')
    print('=' * 60)


if __name__ == '__main__':
    update_encyclopedia()
