"""
用户扩展模型 - Profile和MBTI
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from clubs.image_utils import center_crop_and_resize_imagefield

User = get_user_model()


class Profile(models.Model):
    """用户扩展信息"""
    GENDER_CHOICES = [
        ('secret', '保密'),
        ('male', '男'),
        ('female', '女'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True,
        verbose_name='头像',
        help_text='建议尺寸 400x400，系统会自动居中裁剪'
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='个人签名',
        help_text='一句话介绍自己，展示在个人主页（500字以内）'
    )
    student_id = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='学号',
        help_text='你的学号'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='手机号',
        help_text='用于接收活动通知'
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='secret',
        verbose_name='性别'
    )
    birthday = models.DateField(
        blank=True,
        null=True,
        verbose_name='生日'
    )
    major = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='专业',
        help_text='所学专业'
    )
    class_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='班级',
        help_text='如：计算机2024级1班'
    )
    personal_url = models.URLField(
        max_length=200,
        blank=True,
        verbose_name='个人网站',
        help_text='个人博客或社交媒体链接'
    )
    mbti_type = models.CharField(
        max_length=4,
        blank=True,
        null=True,
        verbose_name='MBTI性格类型',
        help_text='如：INTJ, ENFP等'
    )

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

    def __str__(self):
        return f'{self.user.username}的资料'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_image:
            center_crop_and_resize_imagefield(self.profile_image, 400, 400)

    @property
    def mbti(self):
        """兼容旧属性名"""
        return self.mbti_type

    @mbti.setter
    def mbti(self, value):
        """兼容旧属性名"""
        self.mbti_type = value


# 信号：当用户创建时自动创建Profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """为新用户自动创建Profile"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """保存用户时同时保存Profile"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
