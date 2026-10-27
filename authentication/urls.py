from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CreateAccountAPIView, VerifyCodeAPIView, CreateTempUserAPIView, LoginAPIView, LogoutAPIView,
    ChangePasswordAPIView, UpdateSettingsAPIView
)

urlpatterns = [
    path('signup', CreateTempUserAPIView.as_view()),
    path('verify-code', VerifyCodeAPIView.as_view()),
    path('create-account', CreateAccountAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('password/change', ChangePasswordAPIView.as_view()),
    path('profile/update', UpdateSettingsAPIView.as_view()),
    
]