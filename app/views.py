from app.middleware import User
import os

from account.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils.encoding import smart_str
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Category, Post, Ip


class PostList(ListView):
    model = Post
    template_name = "app/post_list.html"
    context_object_name = "post_list"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "همه ی عکس ها"
        context["namespace"] = "post_list"
        context["current_page"] = self.kwargs.get("page", 1)
        return context

class PostDetail(DetailView):
    model = Post
    template_name = "app/post_detail.html"
    context_object_name = "post"

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR")

        return ip

    def get_obj(self):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post.objects.all(), slug=slug)
        return obj

    def get_queryset(self):
        ip_obj = Ip.objects.get(ip_address=self.get_client_ip())
        obj = self.get_obj()
        obj.hits.add(ip_obj)
        obj.save()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        global is_downloaded, is_liked
        is_downloaded = False
        is_liked = False
        obj = self.get_obj()

        if self.request.user.is_authenticated:
            username = self.request.user.username
            email = self.request.user.email
            user = User.objects.get(username=username, email=email)

            if user in obj.download_count.all():
                is_downloaded = True

            if user in obj.likes_count.all():
                is_liked = True

        context["is_downloaded"] = is_downloaded
        context["is_liked"] = is_liked
        return context

class PublisherList(ListView):
    template_name = "app/post_list.html"
    context_object_name = "post_list"
    paginate_by = 5

    def get_queryset(self):
        global publisher, username
        username = self.kwargs.get("username")
        publisher = get_object_or_404(User.objects.all(), username=username)
        return publisher.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"عکس های {publisher.get_name_or_username}"
        context["current_page"] = self.kwargs.get("page", 1)
        context["namespace"] = "publisher_list"
        context["username"] = username
        return context

class CategoryList(ListView):
    template_name = "app/post_list.html"
    context_object_name = "post_list"
    paginate_by = 5

    def get_queryset(self):
        global category
        slug = self.kwargs.get("slug")
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.posts.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"دسته بندی {category.title}" 
        context["current_page"] = self.kwargs.get("page", 1)
        context["namespace"] = "category_list"
        context["category_slug"] = category.slug
        return context

class SearchList(ListView):
    template_name = "app/post_list.html"
    context_object_name = "post_list"
    paginate_by = 5

    def get_queryset(self):
        global search_name
        search_name = self.kwargs.get("search")
        query = Post.objects.filter(Q(title__icontains=search_name) | 
        Q(category__title__icontains=search_name))
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"نتیجه جستجوی {search_name}" 
        context["current_page"] = self.kwargs.get("page", 1)
        context["namespace"] = "search_list"
        context["search_name"] = search_name
        return context

class DownloadView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Post.objects.all(), slug=kwargs.get("slug"))
        img = open((settings.DOWNLOAD_ROOT / f"{obj.slug}/{obj.slug}-akscade.jpg"), "rb")
        
        response = HttpResponse(img.read(), content_type="application/force-download")
        response["Content-Disposition"] = f"attachment; filename={os.path.basename(f'{obj.slug}-akscade.jpg')}"
        response["X-Sendfile"] = smart_str(img)

        obj.download_count.add(request.user)
        obj.save()

        return response

class LikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Post.objects.all(), slug=kwargs.get("slug"))
        username = request.user.username
        email = request.user.email
        user = User.objects.get(username=username, email=email)

        if user in obj.likes_count.all():
            obj.likes_count.remove(user)
            return JsonResponse({"action": "dislike", "count": obj.likes_count.count()})
        else:
            obj.likes_count.add(user)
            return JsonResponse({"action": "like", "count": obj.likes_count.count()})