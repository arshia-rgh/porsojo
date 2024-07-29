from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from accounts.serializer import IranianPhoneNumberSerializer, UserRegistrationSerializer, VerifyOtpTokenSerializer
from utils.otp_service import FakeOtpService, KavenegarOtpService


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer


class SendOtpTokenView(generics.GenericAPIView):
    serializer_class = IranianPhoneNumberSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]

        if settings.DEBUG:
            fake_otp_service = FakeOtpService()
            fake_otp_service.send_otp(phone_number)
        else:
            kavenegar_otp_service = KavenegarOtpService(settings.KAVENEGAR_API_TOKEN)
            kavenegar_otp_service.send_otp(phone_number)
        return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)


class VerifyOtpTokenView(generics.GenericAPIView):
    serializer_class = VerifyOtpTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data["phone_number"]
        otp = serializer.validated_data["otp_token"]

        if settings.DEBUG:
            fake_otp_service = FakeOtpService()
            is_verified = fake_otp_service.verify_otp(phone_number, otp)
        else:
            kavenegar_otp_service = KavenegarOtpService(settings.KAVENEGAR_API_TOKEN)
            is_verified = kavenegar_otp_service.verify_otp(phone_number, otp)

        if is_verified:
            try:
                user = authenticate(request, phone_number=phone_number, token=otp)
                token = RefreshToken.for_user(user)
                data = {
                    "refresh": str(token),
                    "access": str(token.access_token),
                }
                return Response(data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
