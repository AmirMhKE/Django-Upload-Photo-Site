from random import randint

from django import template
from django.conf import settings

from ..models import Category

register = template.Library()

@register.inclusion_tag("app/partials/navbar.html")
def category(request):
    number = settings.MAIN_CATEGORIES_NUMBER
    categories = random_categories(number)

    return {
        "request": request,
        "email": settings.EMAIL,
        **categories
    }

def random_categories(num):
    true_categories = Category.objects.active()
    all_categories = Category.objects.all()
    main_categories, other_categories = [], []

    if true_categories.exists():
         # ? Set main categories
        used_position = []
        items_count = (num if len(true_categories) >= num else len(true_categories))

        while len(main_categories) < items_count:
            random_position = randint(0, len(all_categories) - 1)

            if random_position not in used_position:
                used_position.append(random_position)
                obj = Category.objects.get(position=random_position)

                if obj.status:
                    main_categories.append(obj)

        # ? Set other categories
        if len(true_categories) > num:
            for obj in true_categories:
                if obj.position not in used_position:
                    other_categories.append(obj)
                    
            # ? Set other random objects
            other_random_categories, used_indexes = [], []
            while len(other_random_categories) < len(other_categories):
                random_index = randint(0, len(other_categories) - 1)
                
                if random_index not in used_indexes:
                    used_indexes.append(random_index)
                    other_random_categories.append(other_categories[random_index])
        else:
            other_categories = None

        return {
            "category": main_categories,
            "other_category": other_random_categories
        }
    
    return {}
