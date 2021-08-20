from django.urls import path

from .views import (CategoryList, DownloadView, LikeView, LoginView, PostDetail, PostList,
                    PublisherList, SearchList)

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('page/<int:page>/', PostList.as_view(), name='post_list'),
    path('post/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('publisher/<slug:username>/', PublisherList.as_view(), name='publisher_list'),
    path('publisher/<slug:username>/page/<int:page>/', PublisherList.as_view(), 
    name='publisher_list'),
    path('category/<slug:slug>/', CategoryList.as_view(), name='category_list'),
    path('category/<slug:slug>/page/<int:page>/', CategoryList.as_view(), name='category_list'),
    path('search/<str:search>/', SearchList.as_view(), name='search_list'),
    path('search/<str:search>/page/<int:page>/', SearchList.as_view(), name='search_list'),
    path('download/<slug:slug>/', DownloadView.as_view(), name='download'),
    path('like/<slug:slug>/', LikeView.as_view(), name='like'),
    path('login/', LoginView.as_view(), name='login')
]
