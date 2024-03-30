from django.urls import path
from .views import UserListView, UserDetailView, UserRoleUpdateView, UsersRoleView

urlpatterns = [
    path('', UserListView.as_view(), name='users-list-user-create'),
    path('<int:user_id>/', UserDetailView.as_view(), name='user-detail-update-delete'),
    path('roles/', UsersRoleView.as_view(), name='users-roles-list'),
    path('<int:user_id>/roles/', UserRoleUpdateView.as_view(), name='user-role-update'),
]
