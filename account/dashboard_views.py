import json

from app.models import Category, Post
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, View
from extensions.utils import set_default_data_forms

from .forms import PostForm
from .mixins import LoginRequiredMixin

User = get_user_model()

class DashBoardView(LoginRequiredMixin, ListView):
    template_name = "account/dashboard.html"
    context_object_name = "post_list"
    paginate_by = 5

    def get_queryset(self):
        username = self.request.user.username
        user = get_object_or_404(User.objects.all(), username=username)
        return user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_page"] = self.kwargs.get("page", 1)
        context["namespace"] = "dashboard"
        return context

class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "account/post_update.html"
    form_class = PostForm
    success_url = reverse_lazy("account:dashboard")
    context_object_name = "post"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        return get_object_or_404(Post.objects.all(), slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        return context

    def get_form_kwargs(self):
        obj = self.get_object()
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        kwargs["id"] = obj.id
        kwargs["title"] = obj.title
        return kwargs

    def form_valid(self, form):
        obj = form.save()
        get_img = self.request.FILES.get("img")

        if get_img:
            obj.img_save()

        return super().form_valid(form)

    def form_invalid(self, form):
        form.data = set_default_data_forms(form.data.copy(), form.initial.copy())
        return super().form_invalid(form)

class DeletePostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        obj = get_object_or_404(Post.objects.all(), slug=slug)
        obj_id = obj.id

        if obj.publisher == request.user:
            obj.delete()

        event = {"type": "post_deleted", 
        "content": f"عکس شما با عنوان <b>{obj.title}</b> با آیدی <b>{obj_id}</b> با موفقیت حذف شد."}
        request.session["event"] = json.dumps(event)

        success_url = request.GET.get("next") if request.GET.get("next") \
        else redirect("account:dashboard")
        return success_url
        