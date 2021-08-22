from django import template
from django.contrib.auth import get_user_model
from django.db.models import Count, Sum

from ..models import Post

User = get_user_model()

register = template.Library()

def get_download_count():
    query = Post.objects.annotate(download_count=Count("downloads")) \
    .aggregate(download_sum=Sum("download_count"))
    result = query["download_sum"]

    if result is None:
        result = 0

    return result

@register.inclusion_tag("app/partials/public_statistics.html")
def public_statistics(request):
    if request.user.is_authenticated:
        return {
            "request": request,
            "post_count": Post.objects.count(),
            "user_count": User.objects.count(),
            "downloads": get_download_count()
        }

    return {
        "request": request
    }
    