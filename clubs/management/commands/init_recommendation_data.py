# -*- coding: utf-8 -*-
"""
初始化社团推荐系统的示例数据
用法: python manage.py init_recommendation_data
"""

import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from clubs.models import Club, Membership, CrossSchoolEvent
from clubs.recommendation_models import (
    StudentProfile, InterestTag, StudentInterest,
    ClubTag, UserBehavior, ClubRecommendationData
)


class Command(BaseCommand):
    help = '初始化社团推荐系统的示例数据'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='清空现有数据',
        )
    
    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('清空现有数据...')
            self.clear_data()
        
        self.stdout.write('开始初始化数据...')
        
        self.create_interest_tags()
        self.create_sample_students()
        
        self.stdout.write(self.style.SUCCESS('\n数据初始化完成！'))
        self.stdout.write(self.style.SUCCESS('注意：示例社团数据已跳过（Club模型字段不匹配）'))
    
    def clear_data(self):
        """清空数据"""
        InterestTag.objects.all().delete()
        StudentInterest.objects.all().delete()
        UserBehavior.objects.all().delete()
        ClubTag.objects.all().delete()
        ClubRecommendationData.objects.all().delete()
        StudentProfile.objects.all().delete()
    
    def create_interest_tags(self):
        """创建兴趣标签"""
        tags_data = [
            # 体育运动类
            {'name': '篮球', 'category': 'sports', 'description': '团队篮球运动'},
            {'name': '足球', 'category': 'sports', 'description': '蹴鞠足球运动'},
            {'name': '羽毛球', 'category': 'sports', 'description': '隔网羽毛球运动'},
            {'name': '乒乓球', 'category': 'sports', 'description': '小球乒乓球运动'},
            {'name': '网球', 'category': 'sports', 'description': '网球运动'},
            {'name': '游泳', 'category': 'sports', 'description': '水上游泳运动'},
            {'name': '跑步', 'category': 'sports', 'description': '跑步健身'},
            {'name': '健身', 'category': 'sports', 'description': '体能训练健身'},
            {'name': '跆拳道', 'category': 'sports', 'description': '武术格斗'},
            {'name': '瑜伽', 'category': 'sports', 'description': '身心修炼'},
            
            # 文艺表演类
            {'name': '舞蹈', 'category': 'arts', 'description': '舞蹈表演'},
            {'name': '歌唱', 'category': 'arts', 'description': '声乐演唱'},
            {'name': '合唱', 'category': 'arts', 'description': '团体合唱'},
            {'name': '钢琴', 'category': 'arts', 'description': '键盘乐器'},
            {'name': '吉他', 'category': 'arts', 'description': '弦乐弹奏'},
            {'name': '摄影', 'category': 'arts', 'description': '影像记录'},
            {'name': '绘画', 'category': 'arts', 'description': '美术创作'},
            {'name': '书法', 'category': 'arts', 'description': '传统书法'},
            {'name': '话剧', 'category': 'arts', 'description': '戏剧表演'},
            {'name': '主持', 'category': 'arts', 'description': '活动主持'},
            
            # 传统文化类
            {'name': '围棋', 'category': 'culture', 'description': '策略棋类'},
            {'name': '象棋', 'category': 'culture', 'description': '中国传统棋类'},
            {'name': '剪纸', 'category': 'culture', 'description': '民间艺术'},
            {'name': '刺绣', 'category': 'culture', 'description': '针线刺绣'},
            {'name': '汉服', 'category': 'culture', 'description': '传统服饰'},
            {'name': '茶艺', 'category': 'culture', 'description': '茶道文化'},
            {'name': '京剧', 'category': 'culture', 'description': '国粹戏剧'},
            
            # 学术科创类
            {'name': '编程', 'category': 'academic', 'description': '代码开发'},
            {'name': 'Python', 'category': 'academic', 'description': 'Python语言'},
            {'name': 'Java', 'category': 'academic', 'description': 'Java开发'},
            {'name': 'AI人工智能', 'category': 'academic', 'description': '人工智能技术'},
            {'name': '机器人', 'category': 'academic', 'description': '机器人技术'},
            {'name': '无人机', 'category': 'academic', 'description': '无人机技术'},
            {'name': '数据分析', 'category': 'academic', 'description': '数据科学'},
            {'name': '数学建模', 'category': 'academic', 'description': '数学应用'},
            {'name': '物理实验', 'category': 'academic', 'description': '物理研究'},
            
            # 公益实践类
            {'name': '志愿服务', 'category': 'public_welfare', 'description': '公益服务'},
            {'name': '支教', 'category': 'public_welfare', 'description': '教育支援'},
            {'name': '环保', 'category': 'public_welfare', 'description': '环境保护'},
            {'name': '社区服务', 'category': 'public_welfare', 'description': '社区活动'},
            {'name': '无偿献血', 'category': 'public_welfare', 'description': '爱心献血'},
            
            # 兴趣生活类
            {'name': '旅行', 'category': 'interest', 'description': '旅游探索'},
            {'name': '摄影', 'category': 'interest', 'description': '摄影摄像'},
            {'name': '美食', 'category': 'interest', 'description': '美食烹饪'},
            {'name': '咖啡', 'category': 'interest', 'description': '咖啡文化'},
            {'name': '电影', 'category': 'interest', 'description': '影视欣赏'},
            {'name': '音乐', 'category': 'interest', 'description': '音乐欣赏'},
            {'name': '游戏', 'category': 'interest', 'description': '电子游戏'},
            {'name': '电竞', 'category': 'interest', 'description': '电子竞技'},
            {'name': '动漫', 'category': 'interest', 'description': '动画漫画'},
            {'name': '阅读', 'category': 'interest', 'description': '读书学习'},
        ]
        
        created_count = 0
        for tag_data in tags_data:
            tag, created = InterestTag.objects.get_or_create(
                name=tag_data['name'],
                defaults={
                    'category': tag_data['category'],
                    'description': tag_data['description'],
                    'heat': random.randint(10, 100)
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'  创建标签: {tag.name}')
        
        self.stdout.write(f'  共创建 {created_count} 个兴趣标签')
    
    def create_sample_students(self):
        """创建示例学生档案"""
        # 获取一些现有用户
        users = User.objects.all()[:20]
        
        grades = ['1', '2', '3', '4', '5', '6']
        majors = [
            '计算机科学与技术', '软件工程', '人工智能', '数据科学',
            '电子信息工程', '机械工程', '土木工程', '建筑学',
            '金融学', '经济学', '管理学', '市场营销',
            '英语', '日语', '法学', '新闻学',
            '心理学', '教育学', '美术学', '音乐学'
        ]
        academies = [
            '计算机学院', '软件学院', '电子信息学院', '机械学院',
            '土木学院', '建筑学院', '经济管理学院', '外语学院',
            '法学院', '文学院', '艺术学院', '理学院'
        ]
        
        created_count = 0
        for i, user in enumerate(users):
            # 跳过已有档案的用户
            if hasattr(user, 'student_profile'):
                continue
            
            try:
                profile, created = StudentProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'gender': random.choice(['M', 'F', 'O']),
                        'grade': random.choice(grades),
                        'major': random.choice(majors),
                        'academy': random.choice(academies),
                        'phone': f'138{random.randint(10000000, 99999999)}',
                        'bio': f'我是{user.username}，很高兴认识大家！',
                        'active_time': {
                            'morning': random.choice([0.2, 0.5, 0.8]),
                            'afternoon': random.choice([0.3, 0.6, 0.9]),
                            'evening': random.choice([0.5, 0.8, 1.0]),
                            'night': random.choice([0.1, 0.3, 0.5]),
                        }
                    }
                )
                
                if created:
                    # 随机添加兴趣标签
                    all_tags = list(InterestTag.objects.all())
                    selected_tags = random.sample(all_tags, min(random.randint(3, 6), len(all_tags)))
                    
                    for tag in selected_tags:
                        StudentInterest.objects.get_or_create(
                            student=profile,
                            tag=tag,
                            defaults={'weight': random.uniform(0.5, 1.0)}
                        )
                    
                    created_count += 1
                    self.stdout.write(f'  创建学生档案: {user.username}')
                    
            except Exception as e:
                self.stdout.write(f'  创建学生档案失败: {user.username} - {str(e)}')
        
        self.stdout.write(f'  共创建 {created_count} 个学生档案')
