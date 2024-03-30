from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from userapi.models import UserProfile
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication

def validate_access_token(access_token):
    try:
        AccessToken(access_token)
        return True
    except TokenError:
        return False
    
def get_user_id_from_token(token):
    if token:
        try:
            decoded_token = AccessToken(token)
            return decoded_token['user_id']
        except Exception as e:
            return None
    return None


class ProfileView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if not validate_access_token(token):
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        userid = get_user_id_from_token(token)
        print(userid)
        user_profile = User.objects.get(id=userid)

        try:
            user_profile = User.objects.get(id=userid)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile does not exist'}, status=status.HTTP_404_NOT_FOUND)

        user = user_profile

        profile_data = {
            'userid': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        return Response(profile_data)

    def put(self, request):
        token = request.data.get('token')
        if not validate_access_token(token):
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        userid = get_user_id_from_token(token)
        try:
            user = User.objects.get(id=userid)
            # Update profile fields
            if 'email' in request.data:
                user.email = request.data['email']
            if 'first_name' in request.data:
                user.first_name = request.data['first_name']
            if 'last_name' in request.data:
                user.last_name = request.data['last_name']

            user.save()

            return Response({'message': 'Profile updated successfully'})
        except User.DoesNotExist:
            return Response({'error': 'User profile does not exist'}, status=status.HTTP_404_NOT_FOUND)

class RoleView(APIView):

    def post(self, request):
        token = request.data.get('token')
        if not validate_access_token(token):
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        user = request.user
        if isinstance(user, User):
            try:
                user_profile = UserProfile.objects.get(user=user)
                roles = {
                    'user_role': user_profile.role,
                }
                return Response(roles)
            except UserProfile.DoesNotExist:
                return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
