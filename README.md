# cs24-p2-UAP_Three_Musketeers
Code Samurai 2024 - 2nd Round


# API Documentation:
** Auth
1. Request: POST , URLS: http://127.0.0.1:8000/auth/login/
    data: {
        "username": "user name",
        "password": "user password"
    }
2. Request: POST , URLS: http://127.0.0.1:8000/auth/logout/
    data: {
        "refresh": "refresh token getting while login"
    }
3. Request: Post , URLS: http://127.0.0.1:8000/auth/change-password/
    data: {
        "access_token":"access token getting while login",
        "old_password":"old password",
        "new_password":"new password"
    }

