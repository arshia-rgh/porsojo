from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import SendOtpTokenView, UserRegisterView, VerifyOtpTokenView

app_name = "accounts"
urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login_with_username_and_email"),
    path("login/otp/", SendOtpTokenView.as_view(), name="send_otp_token"),
    path("login/otp/verify/", VerifyOtpTokenView.as_view(), name="verify_otp_token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
