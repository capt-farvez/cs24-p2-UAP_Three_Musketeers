from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from userapi.models import UserProfile
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import TokenError

# While login, token will generate
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username is None or password is None:
            return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        
        if user is None:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
        
        login(request, user)
        refresh = RefreshToken.for_user(user)
        access = AccessToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(access),
            'email': user.email,
        })



# While logout, token will be blacklisted
class LogoutView(APIView):
    # permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Blacklist the refresh token
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            pass
        # Blacklist the access token
        try:
            access_token = request.headers['Authorization'].split()[1]
            token = AccessToken(access_token)
            token.blacklist()
        except Exception as e:
            pass

        logout(request)
        return Response({'message': 'Logout successful'})



def validate_access_token(access_token):
    try:
        # Decode the access token
        token = AccessToken(access_token)
        # If decoding is successful, the token is valid
        return True
    except TokenError:
        # If decoding fails, the token is invalid
        return False


class ChangePasswordView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        # Extract data from request body
        token = request.data.get('access_token')
        old_password = request.data.get('old_password')
        new_password1 = request.data.get('new_password1')

        # Validate the token
        if not token:
            return Response({'error': 'JWT token not provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the token is valid
        if not validate_access_token(token):
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Decode the token and extract user information
            decoded_token = AccessToken(token)
            user_id = decoded_token.payload.get('user_id')

            # Retrieve the user from the user_id
            User = get_user_model()
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Validate old password
        if not user.check_password(old_password):
            return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

        # Set new password
        user.set_password(new_password1)
        user.save()

        return Response({'message': 'Password changed successfully'})



class ResetPasswordInitiateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Logic to password reset process
        return Response({'message': 'Password reset initiated'})
    
class ResetPasswordConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Logic to confirm password reset with a token or code
        return Response({'message': 'Password reset confirmed'})
