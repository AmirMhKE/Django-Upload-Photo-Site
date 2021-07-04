import json

from django.shortcuts import redirect

class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            event = {"type": "login_required", "content": None}
            request.session["event"] = json.dumps(event)
            return redirect(request.GET.get("next", "/"))