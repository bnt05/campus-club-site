from django.db import models


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
