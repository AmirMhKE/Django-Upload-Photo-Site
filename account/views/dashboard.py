import json

from account.forms import PostForm
from account.mixins import LoginRequiredMixin, SuperUserOrUserMixin
from app.filters import post_queryset
from app.models import Category, Post
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from extensions.utils import set_default_data_forms

__all__ = (
    "DashBoardView", "PostCreateView", "EditPostView",
    "DeletePostView"
)

User = get_user_model()

# ? Classes
class DashBoardView(LoginRequiredMixin, SuperUserOrUserMixin, ListView):
    template_name = "account/dashboard.html"
    context_object_name = "post_list"
    paginate_by = 5

    def get_publisher(self):
        user = get_publisher(self.request, self.kwargs.get("username"))
        return user

    def get_queryset(self):
        user = self.get_publisher()
        query = user.posts.all()
        queryset = post_queryset(self.request, query)
        return queryset

    def get_context_data(self, **kwargs):
        user = get_publisher(self.request, self.kwargs.get("username"))
        username = self.kwargs.get("username", "شما")
        context = super().get_context_data(**kwargs)
        context["post_count"] = Post.objects.filter(publisher=user).count()
        context["current_page"] = self.kwargs.get("page", 1)
        context["publisher"] = user
        context["namespace"] = "dashboard"
        context["title"] = username
        return context

class PostCreateView(LoginRequiredMixin, SuperUserOrUserMixin, CreateView):
    model = Post
    template_name = "account/post_create.html"
    form_class = PostForm

    def get_publisher(self):
        user = get_publisher(self.request, self.kwargs.get("username"))
        return user

    def get_success_url(self):
        user = self.get_publisher()
        success_url = get_success_url(self.request, user)
        return success_url

    def get_context_data(self, **kwargs):
        user = self.get_publisher()
        username = self.kwargs.get("username", "شما")
        context = super().get_context_data(**kwargs)
        context["namespace"] = "post_create"
        context["title"] = username
        context["publisher"] = user
        return context

    def get_form_kwargs(self):
        user = self.get_publisher()
        kwargs = super().get_form_kwargs()
        kwargs["user"] = user
        kwargs["operation"] = "create"
        return kwargs

    def form_valid(self, form):
        user = self.get_publisher()
        obj = form.save(commit=False)
        obj.publisher = user
        obj.save()

        # ? Set alert
        username = self.kwargs.get("username", "شما")
        post_id, title = obj.id, obj.title
        content = " ".join(f"عکس <b>{username}</b> با عنوان <b>{title}</b> \
        و آیدی <b>{post_id}</b> با موفقیت ایجاد شد.".split())
        event = {"type": "user_post_created", "content": content}
        self.request.session["event"] = json.dumps(event)

        return super().form_valid(form)

class EditPostView(LoginRequiredMixin, SuperUserOrUserMixin, UpdateView):
    model = Post
    template_name = "account/post_update.html"
    form_class = PostForm
    context_object_name = "post"

    def get_publisher(self):
        user = get_publisher(self.request, self.kwargs.get("username"))
        return user

    def get_success_url(self):
        user = self.get_publisher()
        success_url = get_success_url(self.request, user)
        return success_url

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        return get_object_or_404(Post, slug=slug)

    def get_context_data(self, **kwargs):
        user = self.get_publisher()
        username = self.kwargs.get("username", "شما")
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        context["publisher"] = user
        context["title"] = username
        return context

    def get_form_kwargs(self):
        obj = self.get_object()
        user = self.get_publisher()
        kwargs = super().get_form_kwargs()
        kwargs["user"] = user
        kwargs["operation"] = "update"
        kwargs["id"] = obj.id
        return kwargs

    def form_valid(self, form):
        obj = form.save()
        get_img = self.request.FILES.get("img")

        if get_img:
            obj.img_save()

        # ? Set alert
        username = self.kwargs.get("username", "شما")
        content = " ".join(f"عکس <b>{username}</b> با عنوان <b>{obj.title}</b> \
        و آیدی <b>{obj.id}</b> با موفقیت ویرایش شد.".split())
        event = {"type": "user_post_updated", "content": content}
        self.request.session["event"] = json.dumps(event)

        return super().form_valid(form)

    def form_invalid(self, form):
        form.data = set_default_data_forms(form.data.copy(), form.initial.copy())
        return super().form_invalid(form)

class DeletePostView(LoginRequiredMixin, SuperUserOrUserMixin, DeleteView):
    def get_publisher(self):
        user = get_publisher(self.request, self.kwargs.get("username"))
        return user

    def get_success_url(self):
        user = self.get_publisher()
        success_url = get_success_url(self.request, user)
        return success_url

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post, slug=slug)
        return obj

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        username = self.kwargs.get("username", "شما")

        # ? Set alert
        event = {"type": "post_deleted", 
        "content": "عکس <b>{}</b> با عنوان <b>{}</b> با آیدی <b>{}</b> با موفقیت حذف شد.".
        format(username, obj.title, obj.id)}
        request.session["event"] = json.dumps(event)

        return super().delete(request, *args, **kwargs)
        
# ? Functions
def get_publisher(request, username=None):
    if username is None:
        user = User.objects.get(pk=request.user.pk)
    else:
        user = get_object_or_404(User, username__iexact=username)

    return user

def get_success_url(request, dashboard_user):
    user = get_publisher(request, dashboard_user.username)
    if request.user == user:
        success_url = reverse("account:dashboard")
    else:
        success_url = reverse("account:dashboard", 
        kwargs={"username": user.username})

    return success_url        
