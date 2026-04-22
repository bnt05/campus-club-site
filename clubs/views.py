from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.utils import timezone
import datetime
import os

from .forms import (
    ClubForm,
    ClubRatingForm,
    CrossSchoolEventForm,
    EventCreateForm,
    KnowledgeItemForm,
    PostForm,
    RegisterForm,
)
from .models import (
    Club,
    ClubRating,
    CrossSchoolEvent,
    KnowledgeCategory,
    KnowledgeItem,
    Membership,
    Post,
    PostLike,
    PostComment,
)


def home(request):
    latest_events = CrossSchoolEvent.objects.filter(is_public=True).order_by('-created_at')[:5]
    clubs = Club.objects.annotate(member_count=Count('members')).order_by('-created_at')[:8]
    events = CrossSchoolEvent.objects.filter(is_public=True).order_by('-created_at')[:10]
    top_clubs = Club.objects.annotate(avg_score=Avg('ratings__score'), member_count=Count('members')).order_by('-member_count')[:6]
    hot_events = CrossSchoolEvent.objects.annotate(p_cnt=Count('participants')).filter(is_public=True).order_by('-p_cnt')[:5]
    total_clubs = Club.objects.count()
    total_events = CrossSchoolEvent.objects.count()
    total_participants = Membership.objects.count()
    return render(request, 'clubs/home.html', {
        'latest_events': latest_events,
        'clubs': clubs,
        'events': events,
        'top_clubs': top_clubs,
        'hot_events': hot_events,
        'total_clubs': total_clubs,
        'total_events': total_events,
        'total_participants': total_participants,
    })


def index(request):
    category = request.GET.get('category', '')
    clubs = Club.objects.annotate(
        member_count=Count('members'),
        avg_score=Avg('ratings__score'),
        event_count=Count('cross_events')
    )
    if category:
        clubs = clubs.filter(category=category)
    clubs = clubs.order_by('-created_at')
    paginator = Paginator(clubs, 12)
    page = request.GET.get('page', 1)
    clubs = paginator.get_page(page)
    categories = [
        ('sports', '体育竞技类'),
        ('arts', '文艺表演类'),
        ('culture', '传统文化类'),
        ('academic', '学术科创类'),
        ('public_welfare', '公益实践类'),
        ('interest', '兴趣生活类'),
    ]
    return render(request, 'clubs/index.html', {
        'page_obj': clubs,
        'categories': categories,
        'selected_category': category,
    })


club_list = index


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '注册成功，已登录。')
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'clubs/register.html', {'form': form})


@login_required
def profile(request):
    from clubs.profile import Profile
    user_profile, _ = Profile.objects.get_or_create(user=request.user)

    # 处理头像上传
    if request.method == 'POST' and 'upload_avatar' in request.POST:
        avatar = request.FILES.get('avatar')
        if avatar:
            old_avatar = user_profile.profile_image
            user_profile.profile_image = avatar
            try:
                user_profile.save()
            except Exception:
                messages.error(request, '头像更新失败，请重试。')
                return redirect('profile')
            if old_avatar:
                try:
                    old_path = old_avatar.path
                    if old_path and os.path.exists(old_path):
                        os.remove(old_path)
                except Exception:
                    pass
            messages.success(request, '头像更新成功！')
            return redirect('profile')

    # 处理个人信息更新
    if request.method == 'POST' and 'update_profile' in request.POST:
        # 更新User模型字段
        new_username = request.POST.get('username', '').strip()
        if new_username and new_username != request.user.username:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            if User.objects.filter(username=new_username).exclude(id=request.user.id).exists():
                messages.error(request, '用户名已被占用！')
            else:
                request.user.username = new_username
                request.user.save(update_fields=['username'])
                messages.success(request, '用户名已更新！')

        # 更新Profile字段
        user_profile.bio = request.POST.get('bio', '').strip()
        user_profile.student_id = request.POST.get('student_id', '').strip()
        user_profile.phone = request.POST.get('phone', '').strip()
        user_profile.gender = request.POST.get('gender', 'secret')
        user_profile.major = request.POST.get('major', '').strip()
        user_profile.class_name = request.POST.get('class_name', '').strip()
        user_profile.personal_url = request.POST.get('personal_url', '').strip()

        birthday_str = request.POST.get('birthday', '').strip()
        if birthday_str:
            from datetime import datetime
            try:
                user_profile.birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
            except ValueError:
                try:
                    user_profile.birthday = datetime.strptime(birthday_str, '%Y/%m/%d').date()
                except ValueError:
                    user_profile.birthday = None
        else:
            user_profile.birthday = None

        try:
            user_profile.save()
            messages.success(request, '个人信息已更新！')
        except Exception:
            messages.error(request, '个人信息更新失败，请重试。')
        return redirect('profile')

    # 获取用户加入的社团
    user_memberships = Membership.objects.filter(user=request.user).select_related('club')
    joined_clubs = [m.club for m in user_memberships]
    
    # 获取用户参与的活动
    joined_events = request.user.joined_events.filter(is_public=True).order_by('-created_at')[:10]
    
    # 获取用户创建的活动
    created_events = CrossSchoolEvent.objects.filter(creator=request.user).order_by('-created_at')[:10]
    
    return render(request, 'clubs/profile.html', {
        'user': request.user,
        'joined_clubs': joined_clubs,
        'joined_events': joined_events,
        'created_events': created_events,
    })


@login_required
def club_create(request):
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES)
        if form.is_valid():
            club = form.save(commit=False)
            club.creator = request.user
            club._initial_creator = request.user
            club.save()
            messages.success(request, '社团创建成功。')
            return redirect('club_detail', club_id=club.id)
    else:
        form = ClubForm()
    return render(request, 'clubs/club_form.html', {'form': form, 'title': '创建社团'})


@login_required
def club_edit(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if club.creator != request.user:
        messages.warning(request, '只有社团创建者可以编辑简介。')
        return redirect('club_detail', club_id=club.id)
    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES, instance=club)
        if form.is_valid():
            form.save()
            messages.success(request, '社团简介已更新。')
            return redirect('club_detail', club_id=club.id)
    else:
        form = ClubForm(instance=club)
    return render(request, 'clubs/club_form.html', {'form': form, 'title': '编辑社团'})


@login_required
def toggle_admin(request, club_id, user_id):
    club = get_object_or_404(Club, id=club_id)
    target_user = get_object_or_404(Membership, club=club, user_id=user_id).user
    membership = Membership.objects.filter(club=club, user=target_user).first()
    if club.creator != request.user and not club.is_admin(request.user):
        messages.warning(request, '只有社团管理员可以管理权限。')
        return redirect('club_detail', club_id=club.id)
    if membership:
        membership.is_admin = not membership.is_admin
        membership.save()
        status = '升为管理员' if membership.is_admin else '撤销管理员'
        messages.success(request, f'{target_user.username} 已{status}。')
    return redirect('club_detail', club_id=club.id)


@login_required
def club_join(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if not club.members.filter(id=request.user.id).exists():
        Membership.objects.create(club=club, user=request.user)
        messages.success(request, f'已成功加入{club.name}！')
    return redirect('club_detail', club_id=club.id)


@login_required
def club_leave(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    membership = Membership.objects.filter(club=club, user=request.user).first()
    if membership:
        membership.delete()
        messages.success(request, f'已退出{club.name}。')
    return redirect('club_detail', club_id=club.id)


@login_required
def post_like(request, club_id, post_id):
    post = get_object_or_404(Post, id=post_id, club_id=club_id)
    like, created = PostLike.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect('club_detail', club_id=club_id)


@login_required
def post_comment(request, club_id, post_id):
    post = get_object_or_404(Post, id=post_id, club_id=club_id)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            PostComment.objects.create(post=post, author=request.user, content=content)
            messages.success(request, '评论已发布。')
    return redirect('club_detail', club_id=club_id)


@login_required
def post_pin(request, club_id, post_id):
    post = get_object_or_404(Post, id=post_id, club_id=club_id)
    club = post.club
    if club.creator == request.user or club.is_admin(request.user):
        post.is_pinned = not post.is_pinned
        post.save()
        status = '置顶' if post.is_pinned else '取消置顶'
        messages.success(request, f'动态已{status}。')
    return redirect('club_detail', club_id=club_id)


def club_detail(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    is_member = request.user.is_authenticated and club.members.filter(id=request.user.id).exists()
    is_admin = club.is_admin(request.user) if request.user.is_authenticated else False
    posts = club.posts.select_related('author').prefetch_related('likes', 'comments__author').all()[:20]
    ratings = club.ratings.select_related('user').all()
    avg_score = club.average_score()
    user_rating = None
    if request.user.is_authenticated:
        user_rating = ClubRating.objects.filter(club=club, user=request.user).first()
    knowledge_categories = club.knowledge_categories.prefetch_related('items').all()
    cross_events = club.cross_events.filter(is_public=True)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if 'join_club' in request.POST:
                if not is_member:
                    Membership.objects.create(club=club, user=request.user)
                    messages.success(request, f'已成功加入{club.name}！')
                return redirect('club_detail', club_id=club.id)
            elif 'leave_club' in request.POST:
                if is_member:
                    Membership.objects.filter(club=club, user=request.user).delete()
                    messages.success(request, f'已退出{club.name}。')
                return redirect('club_detail', club_id=club.id)
            elif 'rate_club' in request.POST:
                score = int(request.POST.get('score', 0))
                if 1 <= score <= 5:
                    rating, created = ClubRating.objects.update_or_create(
                        club=club, user=request.user,
                        defaults={'score': score}
                    )
                    if created:
                        messages.success(request, '感谢您的评分！')
                    else:
                        messages.success(request, '您的评分已更新！')
                return redirect('club_detail', club_id=club.id)
    return render(request, 'clubs/club_detail.html', {
        'club': club,
        'is_member': is_member,
        'is_admin': is_admin,
        'is_owner': club.creator == request.user,
        'posts': posts,
        'ratings': ratings,
        'avg_score': avg_score,
        'user_rating': user_rating,
        'knowledge_categories': knowledge_categories,
        'cross_events': cross_events,
        'post_form': PostForm(),
        'rating_form': ClubRatingForm(instance=user_rating, club=club, user=request.user),
    })


@login_required
def my_clubs(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_clubs = Club.objects.filter(
        Q(creator=request.user) | Q(membership__user=request.user)
    ).distinct()
    created_clubs = user_clubs.filter(creator=request.user)
    joined_clubs = user_clubs.filter(membership__user=request.user).exclude(creator=request.user)
    return render(request, 'clubs/my_clubs.html', {
        'created_clubs': created_clubs,
        'joined_clubs': joined_clubs,
    })


@login_required
def post_create(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if not club.members.filter(id=request.user.id).exists():
        messages.warning(request, '只有社团成员可以发布动态。')
        return redirect('club_detail', club_id=club.id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.club = club
            post.author = request.user
            post.save()
            messages.success(request, '动态已发布。')
            return redirect('club_detail', club_id=club.id)
    else:
        form = PostForm()
    return redirect('club_detail', club_id=club.id)


@login_required
def knowledge_item_create(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if not club.members.filter(id=request.user.id).exists():
        messages.warning(request, '只有社团成员可以添加知识共享内容。')
        return redirect('club_detail', club_id=club.id)
    if not club.knowledge_categories.exists():
        KnowledgeCategory.objects.create(club=club, name='默认分类')
    if request.method == 'POST':
        form = KnowledgeItemForm(request.POST, request.FILES)
        form.fields['category'].queryset = club.knowledge_categories.all()
        if form.is_valid():
            item = form.save(commit=False)
            item.uploaded_by = request.user
            item.save()
            messages.success(request, '知识文档已添加。')
            return redirect('club_detail', club_id=club.id)
    else:
        form = KnowledgeItemForm()
        form.fields['category'].queryset = club.knowledge_categories.all()
    return render(request, 'clubs/knowledge_item_form.html', {
        'club': club,
        'form': form,
        'title': '添加知识文档',
    })


@login_required
def cross_school_event_create(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if not club.is_admin(request.user) and club.creator != request.user:
        messages.warning(request, '只有社团管理员可以发布跨校活动。')
        return redirect('club_detail', club_id=club.id)
    if request.method == 'POST':
        form = CrossSchoolEventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.club = club
            event.save()
            messages.success(request, '跨校活动已发布。')
            return redirect('club_detail', club_id=club.id)
    else:
        form = CrossSchoolEventForm()
    return render(request, 'clubs/cross_school_event_form.html', {
        'club': club,
        'form': form,
        'title': '发布跨校活动',
    })


@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventCreateForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            event = form.save(commit=False)
            club = form.cleaned_data.get('club')
            scope = form.cleaned_data.get('scope')
            
            # 只有社团活动才需要选择社团
            if scope == 'club_activity':
                if not club:
                    messages.error(request, '请选择发布社团。')
                    return render(request, 'clubs/event_create.html', {
                        'form': form,
                        'title': '创建活动',
                    })
                if club.creator != request.user:
                    messages.error(request, '只能选择你创建的社团发布活动。')
                    return render(request, 'clubs/event_create.html', {
                        'form': form,
                        'title': '创建活动',
                    })
            
            event.club = club
            event.creator = request.user
            event.save()
            messages.success(request, '校园活动创建成功。')
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventCreateForm(user=request.user)
    return render(request, 'clubs/event_create.html', {
        'form': form,
        'title': '创建活动',
    })


@login_required
def event_edit(request, event_id):
    event = get_object_or_404(CrossSchoolEvent, id=event_id)
    # 检查权限：只有活动创建者可以编辑
    if event.creator != request.user:
        messages.warning(request, '只有活动创建者可以编辑该活动。')
        return redirect('event_detail', event_id=event.id)
    if request.method == 'POST':
        form = CrossSchoolEventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, '活动信息已更新。')
            return redirect('event_detail', event_id=event.id)
    else:
        form = CrossSchoolEventForm(instance=event)
    return render(request, 'clubs/event_create.html', {
        'form': form,
        'title': '编辑活动',
    })


@login_required
def event_delete(request, event_id):
    event = get_object_or_404(CrossSchoolEvent, id=event_id)
    # 只有活动创建者可以删除活动
    if event.creator != request.user:
        messages.error(request, '只有活动创建者可以删除该活动。')
        return redirect('event_detail', event_id=event.id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, '活动已删除。')
        return redirect('my_events')
    return render(request, 'clubs/event_confirm_delete.html', {
        'event': event,
    })


@login_required
def my_events(request):
    joined_events = request.user.joined_events.filter(is_public=True).order_by('-created_at')
    managed_clubs = Club.objects.filter(
        Q(creator=request.user) | Q(membership__user=request.user, membership__is_admin=True)
    ).distinct()
    published_events = CrossSchoolEvent.objects.filter(club__in=managed_clubs).order_by('-created_at')
    return render(request, 'clubs/my_events.html', {
        'joined_events': joined_events,
        'published_events': published_events,
    })


@login_required
def event_join(request, event_id):
    event = get_object_or_404(CrossSchoolEvent, id=event_id, is_public=True)
    if event.is_full and request.user not in event.participants.all():
        messages.warning(request, '该活动报名人数已达上限。')
    else:
        event.participants.add(request.user)
        messages.success(request, '已报名活动。')
    return redirect('event_detail', event_id=event.id)


@login_required
def event_leave(request, event_id):
    event = get_object_or_404(CrossSchoolEvent, id=event_id, is_public=True)
    event.participants.remove(request.user)
    messages.success(request, '已取消报名。')
    return redirect('event_detail', event_id=event.id)


def events_list(request):
    events = CrossSchoolEvent.objects.filter(is_public=True).order_by('-created_at')
    paginator = Paginator(events, 12)
    page = request.GET.get('page', 1)
    events = paginator.get_page(page)
    return render(request, 'clubs/events_list.html', {'page_obj': events})


def event_detail(request, event_id):
    event = get_object_or_404(CrossSchoolEvent, id=event_id)
    is_joined = request.user in event.participants.all() if request.user.is_authenticated else False
    can_edit = request.user.is_authenticated and event.creator == request.user
    if request.user.is_authenticated and 'join_event' in request.POST:
        if not event.is_full or is_joined:
            event.participants.add(request.user)
            messages.success(request, '已成功报名该活动！')
            return redirect('event_detail', event_id=event.id)
    if request.user.is_authenticated and 'leave_event' in request.POST:
        event.participants.remove(request.user)
        messages.success(request, '已取消报名。')
        return redirect('event_detail', event_id=event.id)
    related_events = CrossSchoolEvent.objects.filter(
        is_public=True,
        category=event.category
    ).exclude(id=event.id)[:4]
    return render(request, 'clubs/event_detail.html', {
        'event': event,
        'is_joined': is_joined,
        'can_edit': can_edit,
        'related_events': related_events,
    })


def event_ical(request, event_id):
    event = get_object_or_404(CrossSchoolEvent, id=event_id)
    try:
        import icalendar
        calendar = icalendar.Calendar()
        event_ical = icalendar.Event()
        event_ical.add('summary', event.title)
        event_ical.add('description', event.description)
        event_ical.add('dtstart', event.start_date)
        event_ical.add('dtend', event.end_date or event.start_date)
        event_ical.add('location', event.location)
        calendar.add_component(event_ical)
        response = HttpResponse(calendar.to_ical(), content_type='text/calendar')
        response['Content-Disposition'] = f'attachment; filename={event.title}.ics'
        return response
    except:
        return HttpResponse('无法生成日历文件', status=500)


@login_required
def rate_club(request, club_id):
    if request.method == 'POST':
        club = get_object_or_404(Club, id=club_id)
        score = int(request.POST.get('score', 0))
        if 1 <= score <= 5:
            rating, created = ClubRating.objects.update_or_create(
                club=club, user=request.user,
                defaults={'score': score}
            )
            if created:
                messages.success(request, '感谢您的评分！')
            else:
                messages.success(request, '您的评分已更新！')
    return redirect('club_detail', club_id=club_id)


@login_required
def ai_assistant(request):
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            message = data.get('message', '')
            from .ai_service import AIAssistant
            assistant = AIAssistant()
            reply = assistant.chat(message)
            return HttpResponse(json.dumps({'reply': reply}), content_type='application/json')
        except:
            return HttpResponse(json.dumps({'reply': '抱歉，服务暂时不可用。'}), content_type='application/json')
    return HttpResponse(status=405)


@login_required
def mbti_test(request):
    from .ai_service import AIAssistant
    if request.method == 'POST':
        answers = dict(request.POST)
        answers.pop('csrfmiddlewaretoken', None)
        assistant = AIAssistant()
        result = assistant.get_mbti_result(answers)
        return render(request, 'clubs/mbti_result.html', {'result': result})
    questions = AIAssistant.get_mbti_questions()
    return render(request, 'clubs/mbti_test.html', {'questions': questions})


def recommendation_page(request):
    """社团智能推荐页面"""
    return render(request, 'clubs/recommendation_page.html')


def statistics_dashboard(request):
    """数据分析看板页面"""
    return render(request, 'clubs/statistics_dashboard.html')
