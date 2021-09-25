from django import template
from django.conf import settings

from ..models import Category

register = template.Library()

@register.inclusion_tag("app/partials/navbar.html")
def category(request):
    number = settings.MAIN_CATEGORIES_NUMBER
    categories = [*Category.objects.order_by("?").iterator()]

    return {
        "request": request,
        "email": settings.EMAIL,
        "category": categories[:number],
        "other_category": categories[number:]
    }
