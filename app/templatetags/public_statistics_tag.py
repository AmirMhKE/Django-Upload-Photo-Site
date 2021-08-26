from django import template
from django.contrib.auth import get_user_model

from ..models import Post, Download

User = get_user_model()

register = template.Library()

@register.inclusion_tag("app/partials/public_statistics.html")
def public_statistics(request):
    if request.user.is_authenticated:
        return {
            "request": request,
            "post_count": Post.objects.count(),
            "user_count": User.objects.count(),
            "downloads": Download.objects.count()
        }

    return {
        "request": request
    }
    