from django import template
from django.contrib.auth import get_user_model
from django.db.models import Count
from ..models import Post

User = get_user_model()

register = template.Library()

def get_download_count():
    query = Post.objects.annotate(Count("download_count"))
    query = (*query.values_list("download_count__count"),)
    result = sum((count[0] for count in query))
    return result

@register.inclusion_tag("app/partials/public_statistics.html")
def public_statistics(request):
    if request.user.is_authenticated:
        return {
            "request": request,
            "post_count": Post.objects.count(),
            "user_count": User.objects.count(),
            "download_count": get_download_count()
        }

    return {
        "request": request
    }