from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from accounts.models.otp_token import OtpToken
from accounts.serializer import (
    IranianPhoneNumberSerializer,
    PasswordChangeSerializer,
    ProfileSerializer,
    UserRegistrationSerializer,
    VerifyOtpTokenSerializer,
)
from accounts.tasks import send_otp, send_verification_email
from utils.otp_service import BaseOtpService, FakeOtpService, KavenegarOtpService


class UserRegisterView(generics.CreateAPIView):
    """
    View for user registration.

    This view handles the creation of a new user account.
    """

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        send_verification_email.delay(user.id, user.email)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "User registered successfully. Please check your email to verify your account."},
                        status=status.HTTP_201_CREATED)


class SendOtpTokenView(generics.GenericAPIView):
    """
    View for sending One-Time Password (OTP) token.

    This view handles the sending of an OTP token to a phone number.
    """

    serializer_class = IranianPhoneNumberSerializer
    permission_classes = (AllowAny,)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Sends an OTP token to the provided phone number.

        Args:
            request (Request): The Drf request object.

        Returns:
            Response: A response object containing a success message.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number: str = serializer.validated_data["phone_number"]
        OtpToken.check_max_try(phone_number)
        send_otp.delay(phone_number)
        return Response({"message": "OTP sent successfully"}, status=status.HTTP_201_CREATED)


class VerifyOtpTokenView(generics.GenericAPIView):
    """
    View for verifying One-Time Password (OTP) token.

    This view handles the verification of an OTP token.
    """

    serializer_class = VerifyOtpTokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Verifies an OTP token.

        Args:
            request (Request): The DRF request object.

        Returns:
            Response: A response object containing a success message and access token.
            If the OTP token is invalid, a response with a 400 status code is returned.
            If the user is not found, a response with a 404 status code is returned.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number: str = serializer.validated_data["phone_number"]
        otp: str = serializer.validated_data["otp_token"]
        try:
            user: User = authenticate(request, phone_number=phone_number, token=otp)
            token: RefreshToken = RefreshToken.for_user(user)
            data: dict[str, str] = {
                "refresh": str(token),
                "access": str(token.access_token),
            }
            return Response(data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class ProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating the authenticated user's profile.

    This view handles the retrieval and updating of the authenticated user's profile.

    Attributes:
        serializer_class (ProfileSerializer): The serializer class for this view.
        permission_classes (tuple): The permission classes for this view.
        queryset (QuerySet): The queryset for this view.

    Methods:
        get_object() -> User: Returns the authenticated user.
        update(request, *args, **kwargs) -> Response: Updates the authenticated user's profile.
    """

    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects

    def get_object(self):
        """
        Returns the authenticated user.

        Returns:
            User: The authenticated user.
        """
        return self.request.user

    def update(self, request, *args, **kwargs):
        """
        Updates the authenticated user's profile.

        Args:
            request (Request): The DRF request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A response object containing the updated profile data.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ChangePasswordView(generics.UpdateAPIView):
    """
    View for changing the user's password.

    This view handles the changing of the user's password.
    """

    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """
        Get the user object for the current request.

        Returns:
            User: The user object.
        """
        return self.request.user

    def update(self, request, *args, **kwargs):
        """
        Change the user's password.

        Args:
            request (Request): The DRF request object.

        Returns:
            Response: A response object containing a success message.
        """
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.object.set_password(serializer.validated_data["password"])
        self.object.save()
        return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)


class SendEmailVerificationView(generics.GenericAPIView):
    pass
