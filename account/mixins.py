import json

from django.shortcuts import redirect
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            event = {"type": "login_required", "content": None}
            request.session["event"] = json.dumps(event)
            return redirect(request.GET.get("next", request.META.get("HTTP_REFERER", "/")))

class SuperUserOrUserMixin:
    def dispatch(self, request, *args, **kwargs):
        user = User.objects.get(username__iexact=kwargs.get("username", request.user.username))
    
        if not (request.user.username == user.username or request.user.is_superuser): 
            return redirect("/", request.META.get("HTTP_REFERER", "/"))

        return super().dispatch(request, *args, **kwargs)