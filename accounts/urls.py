from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    ChangePasswordView,
    ProfileRetrieveUpdateView,
    SendOtpTokenView,
    UserRegisterView,
    VerifyOtpTokenView,
    VerifyEmailView,
)

app_name = "accounts"
urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("verify-email/<uidb64>/<token>", VerifyEmailView.as_view(), name="verify_email"),
    path("login/", TokenObtainPairView.as_view(), name="login_with_username_and_email"),
    path("login/otp/", SendOtpTokenView.as_view(), name="send_otp_token"),
    path("login/otp/verify/", VerifyOtpTokenView.as_view(), name="verify_otp_token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", ProfileRetrieveUpdateView.as_view(), name="profile"),
    path("profile/password-change/", ChangePasswordView.as_view(), name="change_password"),
]
