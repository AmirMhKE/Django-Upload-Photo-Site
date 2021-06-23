from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import LoginView, SignUpView, ActivateAccount

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<slug:uidb64>/<slug:token>/', ActivateAccount.as_view(), name='activate')
]