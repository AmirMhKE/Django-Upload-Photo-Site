from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import StatisticsView, UserSettingsView, UserDeleteView

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('settings/', UserSettingsView.as_view(), name='settings'),
    path('delete/', UserDeleteView.as_view(), name='user_delete')
]
