import os

from account.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_str
from django.views import View
from django.views.generic import DetailView, ListView
from django.contrib.auth.views import LoginView as LoginView_
from extensions.utils import get_files_list, get_random_str
from PIL import Image

from app.middleware import User

from .models import Category, Ip, Post
from .filters import PostSearchFilter


class PostList(ListView):
    model = Post
    template_name = "app/post_list.html"
    context_object_name = "post_list"
    paginate_by = 5

    def get_queryset(self):
        query = Post.objects.all()
        queryset = post_queryset(self.request, query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = post_title(self.request, "همه ی عکس ها")
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
            ip_address = x_forwarded_for.split(",")[0]
        else:
            ip_address = self.request.META.get("REMOTE_ADDR")

        return ip_address

    def get_obj(self):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post, slug=slug)
        return obj

    def set_ip_hit(self):
        ip_obj = Ip.objects.get(ip_address=self.get_client_ip())
        obj = self.get_obj()
        
        if ip_obj not in obj.hits.all():
            obj.hits.add(ip_obj)
            obj.save()

    def set_user_hit(self):
        user = self.request.user
        obj = self.get_obj()

        if user.is_authenticated and user not in obj.user_hits.all():
            obj.user_hits.add(user)
            obj.save()

    def get_queryset(self):
        self.set_ip_hit()
        self.set_user_hit()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_downloaded, is_liked = False, False
        obj = self.get_obj()

        if self.request.user.is_authenticated:
            username = self.request.user.username
            email = self.request.user.email
            user = User.objects.get(username=username, email=email)

            if user in obj.downloads.all():
                is_downloaded = True

            if user in obj.likes.all():
                is_liked = True

        context["is_downloaded"] = is_downloaded
        context["is_liked"] = is_liked
        return context

class PublisherList(ListView):
    template_name = "app/post_list.html"
    context_object_name = "post_list"
    paginate_by = 5
    publisher, username = None, None

    def get_queryset(self):
        self.username = self.kwargs.get("username")
        self.publisher = get_object_or_404(User, username=self.username)
        query = self.publisher.posts.all()
        queryset = post_queryset(self.request, query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = post_title(self.request, 
        f"عکس های {self.publisher.get_name_or_username}")
        context["current_page"] = self.kwargs.get("page", 1)
        context["namespace"] = "publisher_list"
        context["username"] = self.username
        return context

class CategoryList(ListView):
    template_name = "app/post_list.html"
    context_object_name = "post_list"
    paginate_by = 5
    category = None

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        self.category = get_object_or_404(Category.objects.active(), slug=slug)
        query = self.category.posts.all()
        queryset = post_queryset(self.request, query)
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = post_title(self.request, 
        f"دسته بندی {self.category.title}") 
        context["current_page"] = self.kwargs.get("page", 1)
        context["namespace"] = "category_list"
        context["category_slug"] = self.category.slug
        return context

class DownloadView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Post, slug=kwargs.get("slug"))
        file_name = get_files_list(os.path.join(settings.DOWNLOAD_ROOT, obj.slug))[-1]
        img = Image.open(file_name)
         
        extension = obj.img.path.split(".")[-1]
        content = \
        f"attachment; filename={os.path.basename(f'{get_random_str(10, 50)}-akscade.{extension}')}" 
        response = HttpResponse(img, content_type="application/force-download")
        response["Content-Disposition"] = content
        response["X-Sendfile"] = smart_str(img)

        obj.downloads.add(request.user)

        return response

class LikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Post, slug=kwargs.get("slug"))
        username = request.user.username
        email = request.user.email
        user = User.objects.get(username=username, email=email)

        if user in obj.likes.all():
            obj.likes.remove(user)
            return JsonResponse({"action": "dislike", "count": obj.likes.count()})

        obj.likes.add(user)
        return JsonResponse({"action": "like", "count": obj.likes.count()})
            
# ? For debug mode
class LoginView(LoginView_):
    template_name = "account/login.html"
    success_url = "/"


# ? Functions
def post_queryset(request, query):
    # ? This function set default query or search or ordering
    if request.GET.get("search") is None:
        queryset = query
    else:
        queryset = PostSearchFilter(request.GET, query).qs

    ordering = request.GET.get("ordering")
    if ordering is not None and ordering in Post.get_model_fields_name():
        queryset = queryset.order_by(ordering)

    return queryset

def post_title(request, default_title):
    # ? For set post title
    search_name = None

    if request.GET.get("search") is not None:
        if request.GET.get("title") or request.GET.get("publisher"):
            search_name = "جستجوی عبارت ' {} ' در {}" \
            .format((request.GET.get('title') or \
            request.GET.get('publisher')), default_title)

    title = search_name or default_title
    return title
