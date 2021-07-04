from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import StatisticsView

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
]
