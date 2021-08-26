from app.filters import PostSearchFilter
from app.models import Category, Download, Hit, Ip, Like, Post, UserHit
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView as LoginView_
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.views.generic import DetailView, ListView

__all__ = (
    "PostList", "PostDetail", "PublisherList", 
    "CategoryList", "LoginView"
)

User = get_user_model()

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
        ip_obj = Ip.objects.get(ip_address=self.get_client_ip())
        hit_query = Hit.objects.filter(post=obj, ip_address=ip_obj)
        
        if not hit_query.exists():
            Hit.objects.create(post=obj, ip_address=ip_obj)

    def set_user_hit(self):
        obj = self.get_object()
        user = self.request.user

        if user.is_authenticated:
            user_hit_query = UserHit.objects.filter(post=obj, user=user)

            if not user_hit_query.exists():
                UserHit.objects.create(post=obj, user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        is_downloaded, is_liked = False, False
        obj = self.get_object()

        if user.is_authenticated:
            like_query = Like.objects.filter(post=obj, user=user)
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

    # ? Ordering filter
    ordering = request.GET.get("ordering", "")
    _ordering = "".join(ordering.split("-"))
    countable_fields = ["hits", "user_hits", "likes", "downloads"]

    if _ordering in Post.get_model_fields_name():
        if _ordering in countable_fields:
            # ? -ordering_count or ordering_count
            ordering_filter_name = f"{ordering}_count"
            # ? -ordering_count -> ordering_count
            ordering_name = f"{_ordering}_count"

            field_annotate = {ordering_name: Count(_ordering)}

            queryset = queryset.annotate(**field_annotate) \
            .order_by(ordering_filter_name)
        else:
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
