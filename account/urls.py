from django.contrib.auth.views import LogoutView
from django.urls import path

from .dashboard_views import (DashBoardView, DeletePostView, EditPostView,
                              PostCreateView)
from .views import (StatisticsView, UserAboutView, UserDeleteView,
                    UserSettingsView)

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('statistics/<slug:username>/', StatisticsView.as_view(), name='statistics'),
    path('settings/', UserSettingsView.as_view(), name='settings'),
    path('settings/<slug:username>/', UserSettingsView.as_view(), name='settings'),
    path('delete/', UserDeleteView.as_view(), name='user_delete'),
    path('about/', UserAboutView.as_view(), name='about'),
    path('about/<slug:username>/', UserAboutView.as_view(), name='about'),
    path('dashboard/', DashBoardView.as_view(), name='dashboard'),
    path('<slug:username>/dashboard/', DashBoardView.as_view(), name='dashboard'),
    path('dashboard/page/<int:page>/', DashBoardView.as_view(), name='dashboard'),
    path('<slug:username>/dashboard/page/<int:page>/', DashBoardView.as_view(), name='dashboard'),
    path('dashboard/delete/<slug:slug>/', DeletePostView.as_view(), name='post_delete'),
    path('<slug:username>/dashboard/delete/<slug:slug>/', 
    DeletePostView.as_view(), name='post_delete'),
    path('dashboard/edit/<slug:slug>/', EditPostView.as_view(), name='post_edit'),
    path('<slug:username>/dashboard/edit/<slug:slug>/', EditPostView.as_view(), name='post_edit'),
    path('dashboard/create/', PostCreateView.as_view(), name='post_create'),
    path('<slug:username>/dashboard/create/', PostCreateView.as_view(), name='post_create'),
]
