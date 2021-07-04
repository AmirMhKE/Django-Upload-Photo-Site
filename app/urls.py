from django.urls import path
from .views import PostList, CategoryList, SearchList, DownloadView

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('page/<int:page>/', PostList.as_view(), name='post_list'),
    path('category/<slug:slug>/', CategoryList.as_view(), name='category_list'),
    path('category/<slug:slug>/page/<int:page>/', CategoryList.as_view(), name='category_list'),
    path('search/<str:search>/', SearchList.as_view(), name='search_list'),
    path('search/<str:search>/page/<int:page>/', SearchList.as_view(), name='search_list'),
    path('download/<slug:slug>/', DownloadView.as_view(), name='download'),
]