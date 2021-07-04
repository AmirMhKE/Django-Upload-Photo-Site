from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from django.utils.encoding import smart_str

from PIL import Image
from account.mixins import LoginRequiredMixin
from .models import Category, Post
import os


class PostList(ListView):
    queryset = Post.objects.published()
    template_name = "app/post_list.html"
    context_object_name = "post_list"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "همه ی عکس ها"
        context["namespace"] = "post_list"
        context["current_page"] = self.kwargs.get("page", 1)
        return context

class CategoryList(ListView):
    template_name = "app/post_list.html"
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
        return context

class SearchList(ListView):
    template_name = "app/post_list.html"
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
        return context

class DownloadView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Post.objects.all(), slug=kwargs.get("slug"))
        dir_name = os.path.dirname(obj.img.path)
        file_name = os.path.join(dir_name, f"{obj.slug}-akscade.jpg")
        img = open(file_name, "rb")
        
        response = HttpResponse(img.read(), content_type="application/force-download")
        response["Content-Disposition"] = f"attachment; filename={os.path.basename(file_name)}"
        response["X-Sendfile"] = smart_str(img)

        obj.download_count.add(request.user)
        obj.save()

        return response