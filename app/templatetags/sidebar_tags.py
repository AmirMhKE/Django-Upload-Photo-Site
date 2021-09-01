import random

from django import template
from django.conf import settings
from django.db.models import Count, Q

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

def suggestion_posts(request, num: int) -> dict:
    """
    This function randomly selects several posts for 
    the user to the desired number from the database.
    """
    all_posts_item = Post.objects.all()
    query = get_most_viewed_category_from_user(request.user) or all_posts_item
        
    # ? Set random items
    random_items = []
    items_count = (num if num <= query.count() else query.count())
    random_items.extend(random.sample([*query], items_count))

    if query is not all_posts_item and query.exists():

        exlude_most_category = all_posts_item \
            .exclude(category__id=query.first().category.id)

        if query.count() < num and exlude_most_category.exists():
            other_items_count = ((num - query.count()) \
            if (num - query.count()) <= exlude_most_category.count() \
            else exlude_most_category.count())

            random_items.extend(random.sample(
            [*exlude_most_category], other_items_count))

    return {
        "title": settings.SIDEBAR_TAG_TITLES["suggestion"],
        "sidebar_items": random_items
    }

def get_most(m2m_column_name: str, title: str, num: int) -> dict:
    """
    This function displays the posts that have 
    the most your m2m to the desired number.
    """
    if m2m_column_name != "likes":
        annotate_dict = {f"{m2m_column_name}_count": Count(m2m_column_name)}
    else:
        annotate_dict = {f"{m2m_column_name}_count": Count(m2m_column_name, 
        filter=Q(likes__status=True))}

    query = Post.objects.alias(**annotate_dict) \
    .order_by(f"-{m2m_column_name}_count", "-created")

    return {
        "title": title,
        "sidebar_items": query[:num],
    }
