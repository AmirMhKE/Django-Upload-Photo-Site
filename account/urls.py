from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import StatisticsView, UserSettingsView, UserDeleteView, login_

urlpatterns = [
    path('login/<str:username>/<str:password>/', login_, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('statistics/<slug:username>/', StatisticsView.as_view(), name='statistics'),
    path('settings/', UserSettingsView.as_view(), name='settings'),
    path('settings/<slug:username>/', UserSettingsView.as_view(), name='settings'),
    path('delete/', UserDeleteView.as_view(), name='user_delete')
]
