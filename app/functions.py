from django.http import HttpRequest

def get_post_list_title(request: HttpRequest, default_title: str) -> str:
    """
    This function set label in post lists page.
    """
    search_name = None

    if request.GET.get("search") is not None:
        if request.GET.get("title") or request.GET.get("publisher"):
            search_name = "جستجوی عبارت ' {} ' در {}" \
            .format((request.GET.get('title') or \
            request.GET.get('publisher')), default_title)

    title = search_name or default_title
    return title
    