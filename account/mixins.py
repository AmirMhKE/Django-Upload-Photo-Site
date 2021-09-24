from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from extension.utils import send_message

from account.functions import check_superuser_or_user_permission
from account.models import AnonymousUser

User = get_user_model()

class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        
        send_message(request, "login_required")
        return redirect(request.GET.get("next", request.META.get("HTTP_REFERER", "/")))

class SuperUserOrUserMixin:
    def dispatch(self, request, *args, **kwargs):
        user = User.objects.filter(username__iexact=kwargs.get("username", request.user.username))
        user = user[0] if user.exists() else AnonymousUser()
    
        if not check_superuser_or_user_permission(request, user): 
            send_message(request, "permission_denied")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        return super().dispatch(request, *args, **kwargs)
