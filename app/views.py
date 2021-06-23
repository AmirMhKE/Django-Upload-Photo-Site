from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.db.models import Q

from .models import Category, Post
from config import settings


class PostList(ListView):
    queryset = Post.objects.published()
    template_name = "post_list.html"
    context_object_name = "post_list"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "همه ی عکس ها"
        context["namespace"] = "post_list"
        context["current_page"] = self.kwargs.get("page", 1)
        context["google_captcha_sitekey"] = settings.GOOGLE_RECAPTCHA_SITE_KEY
        
        try:
            context["event"] = self.request.session.pop("event")
        except KeyError:
            context["event"] = {}

        return context

class CategoryList(ListView):
    template_name = "post_list.html"
    context_object_name = "post_list"
    paginate_by = 5

    def get_queryset(self):
        global category
        slug = self.kwargs.get("slug")
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.posts.published()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"دسته بندی {category.title}" 
        context["current_page"] = self.kwargs.get("page", 1)
        context["namespace"] = "category_list"
        context["category_slug"] = category.slug
        context["google_captcha_sitekey"] = settings.GOOGLE_RECAPTCHA_SITE_KEY
        
        try:
            context["event"] = self.request.session.pop("event")
        except KeyError:
            context["event"] = {}

        return context

class SearchList(ListView):
    template_name = "post_list.html"
    context_object_name = "post_list"
    paginate_by = 5

    def get_queryset(self):
        global search_name
        search_name = self.kwargs.get("search")
        query = Post.objects.filter(Q(title__icontains=search_name) | Q(category__title__icontains=search_name))
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f"نتیجه جستجوی {search_name}" 
        context["current_page"] = self.kwargs.get("page", 1)
        context["namespace"] = "search_list"
        context["search_name"] = search_name
        context["google_captcha_sitekey"] = settings.GOOGLE_RECAPTCHA_SITE_KEY
        
        try:
            context["event"] = self.request.session.pop("event")
        except KeyError:
            context["event"] = {}

        return context