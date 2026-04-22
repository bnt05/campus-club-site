from django import template

register = template.Library()

@register.filter
def is_liked_by(post, user):
    """Check if a post is liked by a specific user"""
    if not user.is_authenticated:
        return False
    return post.likes.filter(user=user).exists()

@register.filter
def get_color(value):
    """Return a Bootstrap color class based on a number"""
    colors = ['primary', 'success', 'info', 'warning', 'danger', 'secondary', 'primary', 'success', 'info', 'warning']
    try:
        index = int(value) % len(colors)
        return colors[index]
    except (ValueError, TypeError):
        return 'primary'
