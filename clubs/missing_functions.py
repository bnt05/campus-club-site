# Missing functions to add to views.py

def index(request):
    """Index page - same as club_list"""
    return club_list(request)


def my_clubs(request):
    """User's joined clubs"""
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


def event_ical(request, event_id):
    event = get_object_or_404(CrossSchoolEvent, id=event_id)
    from django.http import HttpResponse
    import icalendar as icalendar_module
    calendar = icalendar_module.Calendar()
    event_ical = icalendar_module.Event()
    event_ical.add('summary', event.title)
    event_ical.add('description', event.description)
    event_ical.add('dtstart', event.start_date)
    event_ical.add('dtend', event.end_date or event.start_date)
    event_ical.add('location', event.location)
    calendar.add_component(event_ical)
    response = HttpResponse(calendar.to_ical(), content_type='text/calendar')
    response['Content-Disposition'] = f'attachment; filename={event.title}.ics'
    return response


def mbti_test(request):
    from .ai_service import AIAssistant
    if request.method == 'POST':
        answers = request.POST.dict()
        assistant = AIAssistant()
        result = assistant.get_mbti_result(answers)
        return render(request, 'clubs/mbti_result.html', {'result': result})
    questions = AIAssistant.get_mbti_questions()
    return render(request, 'clubs/mbti_test.html', {'questions': questions})
