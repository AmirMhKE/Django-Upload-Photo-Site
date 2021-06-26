from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (ActivateAccount, LoginView, PasswordResetConfirmView,
                    PasswordResetView, SignUpView)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<slug:uidb64>/<slug:token>/', ActivateAccount.as_view(), name='activate'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<slug:uidb64>/<slug:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm')
]
