from app.models import Ip
from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponseNotFound
from django.shortcuts import render
from extension.utils import get_client_ip

__all__ = ("handler404", "handler500")

def _check_template(request: HttpRequest, name: str):
    is_dashboard = False
    
    try:
        if request.path.startswith("/account") and request.user.is_authenticated:
            spl = request.path.split("/account")[1].split("/")
            if spl[1] == "dashboard" or spl[2] == "dashboard":
                is_dashboard = True
    except IndexError:
        pass

    template_name = "account/" + name if is_dashboard else "app/" + name
    context = {"namespace": "", "view": {"kwargs": {}}} if is_dashboard else {}
    return template_name, context

def _check_user_blocking(request: HttpRequest, exception, msg):
    ip_address = get_client_ip(request)
    ip_obj = Ip.objects.get(ip_address=ip_address)
    max_count = settings.MAX_COUNT_EXCESSIVE_REQUESTS

    if ip_obj.excessive_requests_count >= max_count:
        msg_ = str(exception) if type(exception) == Http404 else msg
        return False, msg_

    return True, ""

def handler404(request: HttpRequest, exception):
    msg = "404 Not Found ..."
    check_blocking = _check_user_blocking(request, exception, msg)
    template = _check_template(request, "404.html")

    if not check_blocking[0]:
        return HttpResponseNotFound(check_blocking[1])
    return render(request, template[0], template[1], status=404)

def handler500(request: HttpRequest, exception=None):
    msg = "500 Internal server error ..."
    check_blocking = _check_user_blocking(request, exception, msg)
    template = _check_template(request, "500.html")

    if not check_blocking[0]:
        return HttpResponseNotFound(check_blocking[1])
    return render(request, template[0], template[1], status=500)
