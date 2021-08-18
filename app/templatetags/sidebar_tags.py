from random import randint

from django import template
from django.db.models import Count

from ..models import Post

register = template.Library()

M2M_TITLES = {
    "suggestion": "عکس های پیشنهادی برای شما",
    "popular": "محبوب ترین عکس ها",
    "download": "پر دانلود ترین عکس ها",
    "hit": "پر بازدید ترین عکس ها",
}

@register.inclusion_tag("app/partials/sidebar.html")
def sidebar(request, name, num):
    queries = {
        "suggestion": suggestion_posts,
        "popular": lambda num: get_most("likes", M2M_TITLES["popular"], num),
        "download": lambda num: get_most("downloads", M2M_TITLES["download"], num),
        "hit": lambda num: get_most("hits", M2M_TITLES["hit"], num),
    }

    return {
        "request": request,
        **queries[name](num)
    }

def suggestion_posts(num: int) -> dict:
    """
    This function randomly selects several posts for 
    the user to the desired number from the database.
    """
    query = Post.objects.all()
    random_items = []
        
    # ? Set random items
    used_indexes = []
    items_count = (num if num <= len(query) else len(query))

    while len(random_items) < items_count:
        random_index = randint(0, len(query) - 1)
        if random_index not in used_indexes:
            used_indexes.append(random_index)
            random_items.append(query[random_index])

    return {
        "title": "عکس های پیشنهادی برای شما",
        "sidebar_items": random_items
    }

def get_most(m2m_column_name: str, title: str, num: int) -> dict:
    """
    This function displays the posts that have 
    the most your m2m to the desired number.
    """
    annotate_dict = {f"{m2m_column_name}_count": Count(m2m_column_name)}
    query = Post.objects.annotate(**annotate_dict) \
    .order_by(f"-{m2m_column_name}_count", "-created")

    return {
        "title": title,
        "sidebar_items": query[:num],
    }
