from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from accounts.models.otp_token import OtpToken

UserModel = get_user_model()


class EmailAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):

        if username is None or password is None:
            return None

        try:
            user = UserModel.objects.get(email=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None


class OtpTokenAuthenticationBackend(ModelBackend):
    def authenticate(self, request, token=None, **kwargs):
        if token is None:
            return None

        try:
            otp_token = OtpToken.objects.get(token=token)
            if not otp_token.is_expire:
                try:
                    user = UserModel.objects.get(phone_number=otp_token.phone_number)
                    return user
                except UserModel.DoesNotExist:
                    return None
            return None
        except OtpToken.DoesNotExist:
            return None
