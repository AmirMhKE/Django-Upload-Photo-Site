from .models import Category, Post
from django.views.generic import ListView


class PostList(ListView):
    queryset = Post.objects.published()
    template_name = "home.html"

class CategoryList(ListView):
    model = Category