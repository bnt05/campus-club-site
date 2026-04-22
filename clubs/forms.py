from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import Club, KnowledgeItem, ClubRating, CrossSchoolEvent, Post

User = get_user_model()


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'description', 'category', 'poster']
        labels = {
            'name': '社团名称',
            'description': '社团简介',
            'category': '社团类别',
            'poster': '宣传图片',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入社团名称',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '请输入社团简介...',
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'poster': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '在社团圈中分享你的想法或活动照片...',
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        image = cleaned_data.get('image')
        if not content and not image:
            raise forms.ValidationError('请输入文字内容或上传图片。')
        return cleaned_data


class KnowledgeItemForm(forms.ModelForm):
    class Meta:
        model = KnowledgeItem
        fields = ['category', 'title', 'description', 'document']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '文档标题'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '文档简介'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ClubRatingForm(forms.ModelForm):
    class Meta:
        model = ClubRating
        fields = ['score', 'comment']
        widgets = {
            'score': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '写下你的评价...'}),
        }

    def __init__(self, *args, club=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._club = club
        self._user = user

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self._club:
            instance.club = self._club
        if self._user:
            instance.user = self._user
        if commit:
            instance.save()
        return instance


class CrossSchoolEventForm(forms.ModelForm):
    class Meta:
        model = CrossSchoolEvent
        fields = ['title', 'category', 'scope', 'description', 'location', 'purpose', 'flow', 'precautions', 'poster', 'start_date', 'end_date', 'max_participants', 'is_public']
        labels = {
            'category': '活动标签',
            'scope': '活动级别',
            'location': '活动地点',
            'purpose': '活动目的',
            'flow': '活动流程',
            'precautions': '注意事项',
            'max_participants': '最大报名人数',
            'is_public': '公开活动',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '活动标题'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'scope': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '活动简介'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '活动地点'}),
            'purpose': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '本次活动的目的是什么？'}),
            'flow': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': '活动流程安排'}),
            'precautions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '参加活动前的注意事项'}),
            'poster': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': '填写报名上限'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class EventCreateForm(CrossSchoolEventForm):
    club = forms.ModelChoiceField(
        queryset=Club.objects.none(),
        label='发布社团',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta(CrossSchoolEventForm.Meta):
        fields = ['club'] + CrossSchoolEventForm.Meta.fields

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user is not None:
            self.fields['club'].queryset = Club.objects.filter(creator=self.user)
            if not self.fields['club'].queryset.exists():
                self.fields['club'].help_text = '你还没有创建社团，创建社团后才能以社团名义发起活动。'

    def clean(self):
        cleaned_data = super().clean()
        scope = cleaned_data.get('scope')
        club = cleaned_data.get('club')

        # 只有社团活动才需要选择社团
        if scope == 'club_activity':
            if not club:
                raise forms.ValidationError('请选择发布社团。')
            if club.creator != self.user:
                raise forms.ValidationError('只能选择你创建的社团发布活动。')
        # 其他类型的活动不需要选择社团

        return cleaned_data


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '邮箱'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '确认密码'}),
        }
