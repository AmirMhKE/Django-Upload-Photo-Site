import django_filters

from .models import Post

class PostSearchFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    publisher = django_filters.CharFilter(lookup_expr="username__icontains")

    class Meta:
        model = Post
        fields = ("title", "publisher")
