import json

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, TemplateView, UpdateView, View
from extensions.utils import convert_base64_image_to_django_form_file

from .forms import UserUpdateForm
from .mixins import LoginRequiredMixin, SuperUserOrUserMixin

User = get_user_model()

class StatisticsView(LoginRequiredMixin, SuperUserOrUserMixin, TemplateView):
    template_name = "account/statistics.html"

    def get_context_data(self, **kwargs):
        username = kwargs.get("username", self.request.user.username)

        this_user = User.objects.get(username__iexact=username)
        context = super().get_context_data(**kwargs)
        context.update({
            "username": "شما" if this_user == self.request.user else this_user.get_name_or_username,
            "post_count": this_user.posts.count(),
            "like_count": this_user.likes.count(),
            "all_requests_count": this_user.all_requests_count,
            "requests_search_count": this_user.requests_search_count,
            "requests_download_count": this_user.requests_download_count,
            "excessive_requests_count": this_user.excessive_requests_count,
        })
        return context

class UserSettingsView(LoginRequiredMixin, SuperUserOrUserMixin, UpdateView):
    model = User
    template_name = "account/user_settings.html"
    form_class = UserUpdateForm

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username__iexact=kwargs.get("username", request.user.username))
        username = kwargs.get("username") 
        self.set_profile_image(request)

        # ? Check permission when submit form
        if not any([request.user == user, request.user.is_superuser and not user.is_superuser, 
        request.user.is_admin and not user.is_admin]):
        
            event = {"type": "permission_denied", "content": None}
            request.session["event"] = json.dumps(event)

            if username is None:
                return redirect("account:settings")
            return redirect("account:settings", username)

        return super().post(request, *args, **kwargs)

    def set_profile_image(self, request):
        profile_image = request.POST.get("profile_image")

        if profile_image:
            data = profile_image.split("base64")[1][1:-1] + profile_image.split("base64")[1][-1]
            request.FILES["profile_image"] = convert_base64_image_to_django_form_file(data)

    def get_success_url(self):
        username = self.kwargs.get("username")

        if username is None:
            return reverse("account:settings")
        return reverse("account:settings", kwargs={"username": username})

    def get_object(self):
        username = self.kwargs.get("username") 

        if username is None:
            return User.objects.get(pk=self.request.user.pk)
        return get_object_or_404(User.objects.all(), username__iexact=username)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        kwargs["user"] = User.objects.get(username__iexact=self.kwargs.get("username", self.request.user.username))
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.kwargs.get("username", self.request.user.username))
        context["user"] = user
        context["username"] = "شما" if user == self.request.user else user.get_name_or_username
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

    def get_object(self):
        username = self.kwargs.get("username", self.request.user.username)
        user = get_object_or_404(User.objects.all(), username=username)
        return user

    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context["last_posts"] = user.posts.all()[:6]
        return context