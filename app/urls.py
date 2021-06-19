from django.urls import path
from .views import PostList, CategoryList

urlpatterns = [
    path('', PostList.as_view(), name="post_list"),
    path('page/<int:page>/', PostList.as_view(), name="post_list"),
    path('category/<slug:slug>/', CategoryList.as_view(), name="category_list"),
    path('category/<slug:slug>/page/<int:page>/', CategoryList.as_view(), name="category_list"),
]