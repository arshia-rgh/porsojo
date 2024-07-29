from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core import exceptions

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
    def authenticate(self, request, phone_number=None, token=None, **kwargs):
        if token is None or phone_number is None:
            return None

        try:
            otp_tokens = OtpToken.objects.filter(code=token, phone_number=phone_number)
            if otp_tokens.count() > settings.OTP_MAX_TRY:
                raise exceptions.RequestAborted("Too many otp tokens sent, please try in 30 minutes later.")
            else:
                otp_token = otp_tokens.last()
                if not otp_token.is_expire:
                    try:
                        user = UserModel.objects.get(phone_number=otp_token.phone_number)
                        otp_token.delete()  # delete used otp token
                        return user
                    except UserModel.DoesNotExist:
                        return None
                return None
        except OtpToken.DoesNotExist:
            return None
