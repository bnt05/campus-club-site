from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import EncyclopediaArticle, EncyclopediaCategory


def encyclopedia_home(request):
    category_slug = request.GET.get('category', '')
    query = request.GET.get('q', '')
    articles = EncyclopediaArticle.objects.filter(is_published=True)
    categories = EncyclopediaCategory.objects.all()
    if category_slug:
        articles = articles.filter(category__slug=category_slug)
        current_category = get_object_or_404(EncyclopediaCategory, slug=category_slug)
    else:
        current_category = None
    if query:
        q = Q(title__icontains=query) | Q(content__icontains=query)
        articles = articles.filter(q)
    articles = articles.order_by('-created_at')
    paginator = Paginator(articles, 20)
    page = request.GET.get('page', 1)
    articles = paginator.get_page(page)
    return render(request, 'clubs/encyclopedia_home.html', {
        'page_obj': articles,
        'categories': categories,
        'selected_category': category_slug,
        'current_category': current_category,
        'query': query,
    })


def encyclopedia_category(request, slug):
    category = get_object_or_404(EncyclopediaCategory, slug=slug)
    articles = EncyclopediaArticle.objects.filter(
        category=category,
        is_published=True
    ).order_by('-created_at')
    paginator = Paginator(articles, 20)
    page = request.GET.get('page', 1)
    articles = paginator.get_page(page)
    return render(request, 'clubs/encyclopedia_home.html', {
        'page_obj': articles,
        'categories': EncyclopediaCategory.objects.all(),
        'selected_category': slug,
        'current_category': category,
        'query': '',
    })


def encyclopedia_article(request, slug):
    article = get_object_or_404(EncyclopediaArticle, slug=slug, is_published=True)
    article.views += 1
    article.save(update_fields=['views'])
    related = EncyclopediaArticle.objects.filter(
        category=article.category,
        is_published=True
    ).exclude(id=article.id)[:6]
    return render(request, 'clubs/encyclopedia_article.html', {
        'article': article,
        'related_articles': related,
    })


def encyclopedia_search(request):
    query = request.GET.get('q', '')
    if not query:
        return render(request, 'clubs/encyclopedia_home.html', {
            'page_obj': [],
            'categories': EncyclopediaCategory.objects.all(),
            'selected_category': '',
            'current_category': None,
            'query': '',
        })
    q = Q(title__icontains=query) | Q(summary__icontains=query) | Q(content__icontains=query)
    articles = EncyclopediaArticle.objects.filter(is_published=True).filter(q).order_by('-created_at')
    paginator = Paginator(articles, 20)
    page = request.GET.get('page', 1)
    articles = paginator.get_page(page)
    return render(request, 'clubs/encyclopedia_home.html', {
        'page_obj': articles,
        'categories': EncyclopediaCategory.objects.all(),
        'selected_category': '',
        'current_category': None,
        'query': query,
    })
