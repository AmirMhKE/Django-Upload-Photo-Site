from django.views.generic import TemplateView, UpdateView, View
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .mixins import LoginRequiredMixin
from .forms import UserUpdateForm

User = get_user_model()

class StatisticsView(LoginRequiredMixin, TemplateView):
    template_name = "account/statistics.html"

    def get_context_data(self, **kwargs):
        username = self.request.user.username
        email = self.request.user.email
        this_user = User.objects.get(username=username, email=email)
        context = super().get_context_data(**kwargs)
        context.update({
            "post_count": this_user.posts.count(),
            "like_count": this_user.likes.count(),
            "all_requests_count": this_user.all_requests_count,
            "requests_search_count": this_user.requests_search_count,
            "requests_download_count": this_user.requests_download_count,
            "excessive_requests_count": this_user.excessive_requests_count,
        })
        return context

class UserSettingsView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "account/user_settings.html"
    form_class = UserUpdateForm
    success_url = reverse_lazy("account:settings")

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        kwargs["user"] = self.request.user
        return kwargs

class UserDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.request.user.pk)
        user.delete()
        return redirect("/")