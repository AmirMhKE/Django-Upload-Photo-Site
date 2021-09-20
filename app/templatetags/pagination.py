from django import template
from django.urls import reverse
from extension.utils import param_request_get_to_url_param

register = template.Library()

@register.inclusion_tag("app/partials/pagination.html")
def pagination(request, urlname, **kwargs):
    """
    This template tag for pagination in the all pages.
    page key in view_kwargs should removed because some time
    don't generate url like this --> /example/page/1/page/1/.
    """
    view_kwargs = kwargs.get("view_kwargs", {}).copy()
    view_kwargs.pop("page", {})

    get_url = reverse(urlname, kwargs=view_kwargs)
    context = kwargs.get("context", {})

    return {
        "request": request,
        "get_url": get_url,
        **context
    }

@register.simple_tag
def additional_param(request):
    if request.GET:
        return param_request_get_to_url_param(request.GET)
    return ""
