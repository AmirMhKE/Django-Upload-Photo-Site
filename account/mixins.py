from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from extension.utils import send_message

User = get_user_model()

class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        
        send_message(request, "login_required")
        return redirect(request.GET.get("next", request.META.get("HTTP_REFERER", "/")))

class SuperUserOrUserMixin:
    def dispatch(self, request, *args, **kwargs):
        user = User.objects.get(username__iexact=kwargs.get("username", request.user.username))
    
        if not (request.user == user or (request.user.is_superuser and not user.is_superuser)): 
            return redirect(request.META.get("HTTP_REFERER", "/"))

        return super().dispatch(request, *args, **kwargs)
