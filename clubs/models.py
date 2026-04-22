from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg
from django.utils import timezone
from datetime import timedelta

from clubs.image_utils import center_crop_and_resize_imagefield

User = get_user_model()

# 导入Profile模型（定义在profile.py中）
from clubs.profile import Profile


class Club(models.Model):
    CATEGORY_CHOICES = [
        ('sports', '体育竞技类'),
        ('arts', '文艺表演类'),
        ('culture', '传统文化类'),
        ('academic', '学术科创类'),
        ('public_welfare', '公益实践类'),
        ('interest', '兴趣生活类'),
        ('other', '其他类'),
    ]
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    poster = models.ImageField(upload_to='club_posters/', blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_clubs')
    members = models.ManyToManyField(User, through='Membership', related_name='joined_clubs', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = '社团'
        verbose_name_plural = '社团'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and hasattr(self, '_initial_creator'):
            Membership.objects.create(club=self, user=self.creator, is_admin=True)
        if self.poster:
            center_crop_and_resize_imagefield(self.poster, 1200, 675)

    def add_member(self, user, is_admin=False):
        membership, created = Membership.objects.get_or_create(club=self, user=user)
        if is_admin:
            membership.is_admin = True
            membership.save()
        return membership

    def member_count(self):
        return self.members.count()

    def average_score(self):
        aggregate = self.ratings.aggregate(avg_score=Avg('score'))
        return aggregate['avg_score'] or 0

    def credit_level(self):
        score = self.average_score()
        if score >= 4.5:
            return '优'
        if score >= 3.5:
            return '良'
        if score >= 2.5:
            return '中'
        return '差'

    def get_hotness(self):
        recent_posts = self.posts.filter(created_at__gte=timezone.now() - timedelta(days=30)).count()
        member_count = self.members.count()
        days_since_creation = (timezone.now().date() - self.created_at.date()).days
        time_weight = max(0, 100 - days_since_creation // 10)
        return member_count * 1 + recent_posts * 2 + time_weight

    def is_admin(self, user):
        return self.membership_set.filter(user=user, is_admin=True).exists()

    def membership(self, user):
        return self.membership_set.filter(user=user).first()

    def admins(self):
        return self.members.filter(membership__is_admin=True)


class Membership(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('club', 'user')
        verbose_name = '社团成员'
        verbose_name_plural = '社团成员'

    def __str__(self):
        return f'{self.user.username} in {self.club.name}'


class KnowledgeCategory(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='knowledge_categories')
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class KnowledgeItem(models.Model):
    category = models.ForeignKey(KnowledgeCategory, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    document = models.FileField(upload_to='knowledge_docs/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_knowledge')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = '知识文档'
        verbose_name_plural = '知识文档'

    def __str__(self):
        return self.title


class ClubRating(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='club_ratings')
    score = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('club', 'user')
        verbose_name = '社团评分'
        verbose_name_plural = '社团评分'

    def __str__(self):
        return f'{self.club.name} - {self.score}'


class CrossSchoolEvent(models.Model):
    EVENT_SCOPE_CHOICES = [
        ('club_activity', '社团活动'),
        ('faculty_activity', '院级活动'),
        ('school_activity', '校级活动'),
    ]

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='cross_events', null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events', null=True, blank=True)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=Club.CATEGORY_CHOICES, default='other', verbose_name='活动标签')
    scope = models.CharField(max_length=20, choices=EVENT_SCOPE_CHOICES, default='club_activity', verbose_name='活动级别')
    partner_school = models.CharField(max_length=120, blank=True, default='')
    description = models.TextField(blank=True, verbose_name='活动简介')
    location = models.CharField(max_length=200, blank=True, verbose_name='活动地点')
    purpose = models.TextField(blank=True, verbose_name='活动目的')
    flow = models.TextField(blank=True, verbose_name='活动流程')
    precautions = models.TextField(blank=True, verbose_name='注意事项')
    poster = models.ImageField(upload_to='event_posters/', blank=True, null=True)
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(verbose_name='结束日期')
    max_participants = models.PositiveIntegerField(blank=True, null=True, verbose_name='报名上限')
    participants = models.ManyToManyField(User, related_name='joined_events', blank=True, verbose_name='报名成员')
    is_public = models.BooleanField(default=True, verbose_name='公开活动')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.poster:
            center_crop_and_resize_imagefield(self.poster, 1200, 675)

    @property
    def participant_count(self):
        return self.participants.count()

    @property
    def is_full(self):
        return self.max_participants is not None and self.participant_count >= self.max_participants

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = '跨校活动'
        verbose_name_plural = '跨校活动'

    def __str__(self):
        return self.title


class Post(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='club_posts/', blank=True, null=True)
    is_pinned = models.BooleanField(default=False, verbose_name='置顶')
    pinned_at = models.DateTimeField(null=True, blank=True, verbose_name='置顶时间')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_pinned', '-pinned_at', '-created_at']
        verbose_name = '动态'
        verbose_name_plural = '动态'

    def __str__(self):
        return f'{self.club.name} - {self.author.username}'

    def is_liked_by(self, user):
        if not user.is_authenticated:
            return False
        return self.likes.filter(user=user).exists()


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')
        verbose_name = '动态点赞'
        verbose_name_plural = '动态点赞'

    def __str__(self):
        return f'{self.user.username} liked {self.post}'


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = '动态评论'
        verbose_name_plural = '动态评论'

    def __str__(self):
        return f'{self.author.username} commented on {self.post}'



class EncyclopediaCategory(models.Model):
    """百科分类"""
    name = models.CharField(max_length=50, verbose_name='分类名称')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL别名')
    description = models.TextField(blank=True, verbose_name='分类描述')
    icon = models.CharField(max_length=50, default='bi-book', verbose_name='图标类名')
    order = models.IntegerField(default=0, verbose_name='排序')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '百科分类'
        verbose_name_plural = '百科分类'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class EncyclopediaArticle(models.Model):
    """百科文章"""
    category = models.ForeignKey(
        EncyclopediaCategory,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='所属分类'
    )
    title = models.CharField(max_length=100, verbose_name='文章标题')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL别名')
    summary = models.TextField(verbose_name='简介', blank=True)
    content = models.TextField(verbose_name='正文内容')
    image_url = models.URLField(max_length=500, blank=True, verbose_name='封面图片URL')
    source_url = models.URLField(max_length=500, blank=True, verbose_name='内容来源URL')
    source_name = models.CharField(max_length=100, default='百度百科', verbose_name='来源名称')
    views = models.IntegerField(default=0, verbose_name='浏览次数')
    is_featured = models.BooleanField(default=False, verbose_name='精选')
    is_published = models.BooleanField(default=True, verbose_name='已发布')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '百科文章'
        verbose_name_plural = '百科文章'
        ordering = ['-is_featured', '-views', '-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title
