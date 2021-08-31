import django_filters
from django.db.models import Count, Q

from .models import Post


class PostSearchFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    publisher = django_filters.CharFilter(lookup_expr="username__icontains")

    class Meta:
        model = Post
        fields = ("title", "publisher")

# ? Search or ordering post model
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

            if _ordering != "likes":
                field_annotate = {ordering_name: Count(_ordering)}
            else:
                field_annotate = {ordering_name: Count(_ordering,
                filter=Q(likes__status=True))}

            queryset = queryset.annotate(**field_annotate) \
            .order_by(ordering_filter_name)
        else:
            queryset = queryset.order_by(ordering)

    return queryset
    