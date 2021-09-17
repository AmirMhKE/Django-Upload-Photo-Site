from app.filters import post_queryset
from app.functions import get_post_list_title
from app.models import Category, Download, Hit, Ip, Like, Post, UserHit
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from extensions.utils import get_client_ip

__all__ = (
    "PostList", "PostDetail", "PublisherList", 
    "CategoryList"
)

User = get_user_model()

class PostList(ListView):
    model = Post
    template_name = "app/post_list.html"
    context_object_name = "post_list"
    paginate_by = settings.POST_LIST_PAGE_SIZE

    def get_queryset(self):
        query = Post.objects.all()
        queryset = post_queryset(self.request, query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = get_post_list_title(self.request, "همه ی عکس ها")
        context["namespace"] = "post_list"
        context["current_page"] = self.kwargs.get("page", 1)
        context["side_count"] = settings.SIDEBAR_ITEMS_COUNT
        return context

class PostDetail(DetailView):
    model = Post
    template_name = "app/post_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post, slug=slug)
        return obj

    def get(self, request, *args, **kwargs):
        self.set_ip_hit()
        self.set_user_hit()
        return super().get(request, *args, **kwargs)

    def set_ip_hit(self):
        obj = self.get_object()
        ip_obj = Ip.objects.get(ip_address=get_client_ip(self.request))
        Hit.objects.get_or_create(post=obj, ip_address=ip_obj)

    def set_user_hit(self):
        obj = self.get_object()
        user = self.request.user

        if user.is_authenticated:
            UserHit.objects.get_or_create(post=obj, user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        is_downloaded, is_liked = False, False
        obj = self.get_object()

        if user.is_authenticated:
            like_query = Like.objects.active().filter(post=obj, user=user)
            download_query = Download.objects.filter(post=obj, user=user)

            if like_query.exists():
                is_liked = True

            if download_query.exists():
                is_downloaded = True

        context["is_downloaded"] = is_downloaded
        context["is_liked"] = is_liked
        return context

class PublisherList(ListView):
    template_name = "app/post_list.html"
    context_object_name = "post_list"
    paginate_by = settings.POST_LIST_PAGE_SIZE
    publisher, username = None, None

    def get_queryset(self):
        self.username = self.kwargs.get("username")
        self.publisher = get_object_or_404(User, username=self.username)
        query = self.publisher.posts.all()
        queryset = post_queryset(self.request, query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = get_post_list_title(self.request, 
        f"عکس های {self.publisher.get_name_or_username}")
        context["current_page"] = self.kwargs.get("page", 1)
        context["namespace"] = "publisher_list"
        context["username"] = self.username
        context["side_count"] = settings.SIDEBAR_ITEMS_COUNT
        return context

class CategoryList(ListView):
    template_name = "app/post_list.html"
    context_object_name = "post_list"
    paginate_by = settings.POST_LIST_PAGE_SIZE
    category = None

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        self.category = get_object_or_404(Category.objects.active(), slug=slug)
        query = self.category.posts.all()
        queryset = post_queryset(self.request, query)
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = get_post_list_title(self.request, 
        f"دسته بندی {self.category.title}") 
        context["current_page"] = self.kwargs.get("page", 1)
        context["namespace"] = "category_list"
        context["category_slug"] = self.category.slug
        context["side_count"] = settings.SIDEBAR_ITEMS_COUNT
        return context
