import json

from account.forms import PostForm
from account.functions import (check_number_uploaded_images,
                               check_similar_images, get_dashboard_publisher,
                               get_dashboard_success_url)
from account.mixins import LoginRequiredMixin, SuperUserOrUserMixin
from account.statistics import user_posts_statistics
from app.filters import post_queryset
from app.models import Category, Download, Hit, Like, Post
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)
from extensions.utils import send_message, set_default_data_forms

__all__ = (
    "DashBoardView", "PostCreateView", "EditPostView",
    "DeletePostView", "DashboardStatisticsView"
)

class DashBoardView(LoginRequiredMixin, SuperUserOrUserMixin, ListView):
    template_name = "account/dashboard.html"
    context_object_name = "post_list"
    paginate_by = settings.DASHBOARD_POST_LIST_PAGE_SIZE

    def get_publisher(self):
        user = get_dashboard_publisher(self.request, self.kwargs.get("username"))
        return user

    def get_queryset(self):
        user = self.get_publisher()
        query = user.posts.all()
        queryset = post_queryset(self.request, query)
        return queryset

    def get_context_data(self, **kwargs):
        user = get_dashboard_publisher(self.request, self.kwargs.get("username"))
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

    def post(self, request, *args, **kwargs):
        self.object = None
        
        form = self.get_form()
        form.errors.as_data()
        user = self.get_publisher()
        context = {**self.get_context_data(), "form": form}
        get_image = request.FILES.get("img")
        check_upload = check_number_uploaded_images(Post, user)

        if get_image:
            check_similar = check_similar_images(Post, get_image)

            if not check_similar:
                send_message(self.request, "similar_image_error")
                return self.render_to_response(context)

        if not check_upload[0]:
            content = "شما نمی توانید در هر روز بیشتر از {} عکس آپلود کنید." \
            .format(check_upload[1])
            send_message(self.request, "max_upload_image_error", content)
            return self.render_to_response(context)

        if form.is_valid():
            return self.form_valid(form)
        return self.render_to_response(context)

    def get_publisher(self):
        user = get_dashboard_publisher(self.request, self.kwargs.get("username"))
        return user

    def get_success_url(self):
        user = self.get_publisher()
        success_url = get_dashboard_success_url(self.request, user)
        return success_url

    def get_context_data(self, **kwargs):
        user = self.get_publisher()
        username = self.kwargs.get("username", "شما")
        context = super().get_context_data(**kwargs)
        context["namespace"] = "post_create"
        context["title"] = username
        context["publisher"] = user
        context["img_formats"] = settings.VALID_IMAGE_FORMATS
        context["img_width"] = settings.MIN_IMAGE_WIDTH
        context["img_height"] = settings.MIN_IMAGE_WIDTH
        return context

    def form_valid(self, form):
        user = self.get_publisher()
        obj = form.save(commit=False)
        obj.publisher = user
        obj.save()
        
        username = self.kwargs.get("username", "شما")
        post_id, title = obj.id, obj.title
        content = " ".join(f"عکس <b>{username}</b> با عنوان <b>{title}</b> \
        و آیدی <b>{post_id}</b> با موفقیت ایجاد شد.".split())
        send_message(self.request, "user_post_created", content)

        return super().form_valid(form)

class EditPostView(LoginRequiredMixin, SuperUserOrUserMixin, UpdateView):
    model = Post
    template_name = "account/post_update.html"
    form_class = PostForm
    context_object_name = "post"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()
        context = {**self.get_context_data(), "form": form}
        get_image = request.FILES.get("img")

        if get_image:
            check_similar = check_similar_images(Post, get_image, self.object.pk)

            if not check_similar:
                send_message(request, "similar_image_error")
                return self.render_to_response(context)

        if form.is_valid():
            form = self.form_class(instance=self.object, 
            data=request.POST, files=request.FILES)
            return self.form_valid(form)
        return self.render_to_response(context)

    def get_publisher(self):
        user = get_dashboard_publisher(self.request, self.kwargs.get("username"))
        return user

    def get_success_url(self):
        user = self.get_publisher()
        success_url = get_dashboard_success_url(self.request, user)
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
        context["img_formats"] = settings.VALID_IMAGE_FORMATS
        context["img_width"] = settings.MIN_IMAGE_WIDTH
        context["img_height"] = settings.MIN_IMAGE_WIDTH
        return context

    def form_valid(self, form):
        obj = form.save()
        get_img = self.request.FILES.get("img")

        if get_img:
            obj.img_save()

        # ? Set alert
        username = self.kwargs.get("username", "شما")
        content = " ".join(f"عکس <b>{username}</b> با عنوان <b>{obj.title}</b> \
        و آیدی <b>{obj.id}</b> با موفقیت ویرایش شد.".split())
        send_message(self.request, "user_post_updated", content)

        return super().form_valid(form)

    def form_invalid(self, form):
        form.data = set_default_data_forms(form.data.copy(), form.initial.copy())
        return super().form_invalid(form)

class DeletePostView(LoginRequiredMixin, SuperUserOrUserMixin, DeleteView):
    def get_publisher(self):
        user = get_dashboard_publisher(self.request, self.kwargs.get("username"))
        return user

    def get_success_url(self):
        user = self.get_publisher()
        success_url = get_dashboard_success_url(self.request, user)
        return success_url

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post, slug=slug)
        return obj

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        username = self.kwargs.get("username", "شما")

        content = "عکس <b>{}</b> با عنوان <b>{}</b> با آیدی <b>{}</b> با موفقیت حذف شد." \
        .format(username, obj.title, obj.id)
        send_message(request, "post_deleted", content)

        return super().delete(request, *args, **kwargs)
        
class DashboardStatisticsView(LoginRequiredMixin, SuperUserOrUserMixin, TemplateView):
    template_name = "account/dashboard_statistics.html"

    def get_publisher(self):
        user = get_dashboard_publisher(self.request, self.kwargs.get("username"))
        return user

    def get_context_data(self, **kwargs):
        user = self.get_publisher()
        hit_query = Hit.objects.filter(post__publisher__id=user.id)
        like_query = Like.objects.active().filter(post__publisher__id=user.id)
        download_query = Download.objects.filter(post__publisher__id=user.id)

        context = super().get_context_data(**kwargs)
        context["namespace"] = "dashboard_statistics"
        context["title"] = self.kwargs.get("username", "شما")
        context["stat"] = json.dumps(user_posts_statistics(user, 14))
        context["hits_count"] = hit_query.count()
        context["likes_count"] = like_query.count()
        context["downloads_count"] = download_query.count()
        return context
    