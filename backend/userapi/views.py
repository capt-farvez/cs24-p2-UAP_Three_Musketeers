from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile

class UserListView(APIView):
    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.role == 'System Admin':
                users = User.objects.all()
                user_data = [{'id': user.id, 'username': user.username} for user in users]
                return Response({'users': user_data})
            else:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Authorized profile have to logged in.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.role == 'System Admin':
                username = request.data.get('username')
                email = request.data.get('email')
                password = request.data.get('password')
                role = request.data.get('role', 'Unassigned')

                # Create the user
                user = User.objects.create_user(username=username, email=email, password=password)

                # Create the user profile with the assigned role
                UserProfile.objects.create(user=user, role=role)

                return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Authorized profile have to logged in.'}, status=status.HTTP_404_NOT_FOUND)


class UserDetailView(APIView):
    def get(self, request, user_id):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.role == 'System Admin' or request.user.id == user_id:
                try:
                    user = User.objects.get(id=user_id)
                    user_data = {'id': user.id, 'username': user.username, 'email': user.email}
                    return Response(user_data)
                except User.DoesNotExist:
                    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Authorized profile have to logged in.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, user_id):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.role == 'System Admin' or request.user.id == user_id:
                try:
                    user = User.objects.get(id=user_id)
                    user.username = request.data.get('username', user.username)
                    user.email = request.data.get('email', user.email)
                    user.save()
                    return Response({'message': 'User details updated successfully'})
                except User.DoesNotExist:
                    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Authorized profile have to logged in.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.role == 'System Admin':
                try:
                    user = User.objects.get(id=user_id)
                    user.delete()
                    return Response({'message': 'User deleted successfully'})
                except User.DoesNotExist:
                    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Authorized profile have to logged in.'}, status=status.HTTP_404_NOT_FOUND)


class UserRoleUpdateView(APIView):
    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.role == 'System Admin':
                roles = UserProfile.ROLE_CHOICES
                role_data = [{'name': role[0], 'display_name': role[1]} for role in roles]
                return Response({'roles': role_data})
            else:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Authorized profile have to logged in.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, user_id):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if user_profile.role == 'System Admin':
                try:
                    user = User.objects.get(id=user_id)

                    # Update the user profile role
                    user_profile = UserProfile.objects.get(user=user)
                    role = request.data.get('role')
                    if role:
                        user_profile.role = role
                        user_profile.save()

                    return Response({'message': 'User roles updated successfully'})
                except User.DoesNotExist:
                    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Authorized profile have to logged in.'}, status=status.HTTP_404_NOT_FOUND)
