from app.filters import PostOrderingFilter
from django import template
from django.conf import settings
from django.db.models import Count, QuerySet
from django.http import HttpRequest

from ..models import Category, Post

register = template.Library()

@register.inclusion_tag("app/partials/sidebar.html")
def sidebar(request, name, num):
    queries = {
        "suggestion": lambda num: suggestion_posts(request, num),
        "popular": lambda num: get_most("likes", settings.SIDEBAR_TAG_TITLES["popular"], num),
        "download": lambda num: get_most("downloads", settings.SIDEBAR_TAG_TITLES["download"], num),
        "hit": lambda num: get_most("hits", settings.SIDEBAR_TAG_TITLES["hit"], num),
    }

    return {
        "request": request,
        **queries[name](num)
    }

def get_most_viewed_category_from_user(user):
    """
    This function, if the user is logged in to the site, 
    shows the most categories that the user has visited, 
    the posts related to that category.
    """
    if user.is_authenticated:
        try:
            query = Post.objects.filter(category__id=(
                Category.objects.filter(posts__user_hits__user__id=user.id) \
                .annotate(category_count=Count("posts")) \
                .values("id", "category_count").order_by("-category_count") \
                .first()["id"]
            ))
            return query
        except TypeError:
            pass

    return None

def suggestion_posts(request: HttpRequest, num: int) -> dict[str, list[QuerySet]]:
    """
    This function randomly selects several posts for 
    the user to the desired number from the database.
    """
    all_posts_item = Post.objects.all()
    query = get_most_viewed_category_from_user(request.user) or all_posts_item
        
    # ? Set random items
    random_items = []
    random_items.extend(query.order_by("?")[:num].iterator())

    if query is not all_posts_item and query.exists():
        exlude_most_category = all_posts_item \
        .exclude(category__id=query.first().category.id)
        
        if query.count() < num and exlude_most_category.exists():
            items_count = num - query.count()
            random_items.extend(exlude_most_category.order_by("?")
            [:items_count].iterator())

    return {
        "title": settings.SIDEBAR_TAG_TITLES["suggestion"],
        "sidebar_items": random_items
    }

def get_most(m2m_column_name: str, title: str, num: int) -> dict[str, QuerySet]:
    """
    This function displays the posts that have 
    the most your m2m to the desired number.
    """
    posts = Post.objects.all()
    query = PostOrderingFilter.filter(posts, "-" + m2m_column_name).order_by("-created")

    return {
        "title": title,
        "sidebar_items": query[:num],
    }
