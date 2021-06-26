from django import template
from ..models import Post
from random import randint

register = template.Library()

@register.inclusion_tag("app/partials/sidebar.html")
def sidebar(num):
        suggestion_items = set_suggestion_posts(num)

        return {
            "suggestion_items": suggestion_items
        }

def set_suggestion_posts(num):
    num = int(num)
    query = Post.objects.published()
    random_items = []
        
    # Set random items
    used_indexes = []
    set_num = (num if num <= len(query) else len(query))

    while len(random_items) < set_num:
        random_index = randint(0, len(query) - 1)
        if random_index not in used_indexes:
            used_indexes.append(random_index)
            random_items.append(query[random_index])

    return random_items