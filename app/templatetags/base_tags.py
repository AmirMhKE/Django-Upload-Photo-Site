from random import randint

from django import template

from ..models import Category

register = template.Library()

@register.inclusion_tag("partials/navbar.html")
def category():
    categories = random_categories(5)

    return {
        "category": categories["category"],
        "other_category": categories["other_category"]
    }

def random_categories(num):
    main_categories_number = num
    true_categories = Category.objects.active()
    all_categories = Category.objects.all()
    main_categories, other_categories = [], []

    # Set main categories
    used_position = []
    mains_number = (main_categories_number if len(true_categories) >= main_categories_number 
    else len(true_categories))

    while len(main_categories) < mains_number:
        random_position = randint(0, len(all_categories) - 1)
        if random_position not in used_position:
            used_position.append(random_position)
            obj = Category.objects.get(position=random_position)
            if obj.status:
                main_categories.append(obj)

    # Set other categories
    if len(true_categories) > main_categories_number:
        for obj in true_categories:
            if obj.position not in used_position:
                other_categories.append(obj)
    else:
        other_categories = None

    return {
        "category": main_categories,
        "other_category": other_categories
    }