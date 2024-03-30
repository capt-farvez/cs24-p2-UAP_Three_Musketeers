from django.urls import path
from .views import ProfileView, RoleView

urlpatterns = [
    path('', ProfileView.as_view(), name='profile-view-update'),
    path('role/', RoleView.as_view(), name='user-role'),
]
