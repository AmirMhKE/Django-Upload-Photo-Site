from account.forms import UserUpdateForm
from account.mixins import LoginRequiredMixin, SuperUserOrUserMixin
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, TemplateView, UpdateView, View
from extension.utils import set_default_data_forms, send_message

__all__ = (
    "StatisticsView", "UserSettingsView", "UserDeleteView",
    "UserAboutView"
)

User = get_user_model()

class StatisticsView(LoginRequiredMixin, SuperUserOrUserMixin, TemplateView):
    template_name = "account/statistics.html"

    def get_context_data(self, **kwargs):
        username = kwargs.get("username", self.request.user.username)

        this_user = User.objects.prefetch_related("posts", "likes", "hits") \
        .get(username__iexact=username)

        context = super().get_context_data(**kwargs)
        context.update({
            "username": "شما" if this_user == self.request.user else this_user.get_name_or_username,
            "post_count": this_user.posts.count(),
            "like_count": this_user.likes.active().count(),
            "hits_count": this_user.hits.count(),
            "all_requests_count": this_user.all_requests_count,
            "requests_download_count": this_user.requests_download_count,
            "excessive_requests_count": this_user.excessive_requests_count,
        })
        return context

class UserSettingsView(LoginRequiredMixin, SuperUserOrUserMixin, UpdateView):
    model = User
    template_name = "account/user_settings.html"
    form_class = UserUpdateForm
    
    def form_valid(self, form):
        # ? Set alert
        content = ""
        user = self.get_object()
        
        if user == self.request.user:
            content = "حساب کاربری شما با موفقیت ویرایش شد."
        else:
            content = f"حساب کاربری {user} با موفقیت ویرایش شد."

        send_message(self.request, "user_profile_updated", content)
        
        return super().form_valid(form)

    def form_invalid(self, form):
        form.data = set_default_data_forms(form, form.data.copy(), form.initial.copy())
        return super().form_invalid(form)

    def get_success_url(self):
        username = self.kwargs.get("username")

        if username is None:
            return reverse("account:settings")
        return reverse("account:settings", kwargs={"username": username})

    def get_object(self, queryset=None):
        username = self.kwargs.get("username") 

        if username is None:
            return User.objects.get(pk=self.request.user.pk)
        return get_object_or_404(User, username__iexact=username)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.kwargs.get(
        "username", self.request.user.username))
        context["user"] = user
        context["username"] = "شما" if user == self.request.user else user.get_name_or_username
        context["img_formats"] = settings.VALID_IMAGE_FORMATS
        context["img_width"] = settings.MIN_IMAGE_WIDTH
        context["img_height"] = settings.MIN_IMAGE_WIDTH
        return context

class UserDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.request.user.pk)
        user.delete()
        return redirect("/")

class UserAboutView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "account/user_about.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        username = self.kwargs.get("username", self.request.user.username)
        user = get_object_or_404(User.objects.prefetch_related("posts"), 
        username__iexact=username)
        return user

    def get_context_data(self, **kwargs):
        user = self.get_object()
        post_count = settings.USER_LAST_POSTS_COUNT
        context = super().get_context_data(**kwargs)
        context["last_posts"] = [*user.posts.all().iterator()][:post_count]
        return context
