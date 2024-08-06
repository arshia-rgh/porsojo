from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver

from analytics.models.activities import UserActivity

from ..utils.client_ip_service import get_client_ip
from .constants import LOGIN, LOGIN_FAILED


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    message = f"{user.full_name} is logged in with ip:{get_client_ip(request)}"
    UserActivity.objects.create(user=user, action_type=LOGIN, remarks=message)


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    message = f"Login Attempt Failed for number {credentials.get('phone_number')} with ip: {get_client_ip(request)}"
    UserActivity.objects.create(action_type=LOGIN_FAILED, remarks=message)
