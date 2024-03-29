
from django.urls import path
from .views import LoginView, LogoutView, ResetPasswordInitiateView, ResetPasswordConfirmView, ChangePasswordView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset-password/initiate/', ResetPasswordInitiateView.as_view(), name='reset-password-initiate'),
    path('reset-password/confirm/', ResetPasswordConfirmView.as_view(), name='reset-password-confirm'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

]