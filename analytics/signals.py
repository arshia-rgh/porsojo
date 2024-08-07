from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
from django.db.models.signals import  post_save
from analytics.models.activities import UserActivity
from analytics.constants import READ
from utils.client_ip_service import get_client_ip
from .constants import LOGIN, LOGIN_FAILED
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.contenttypes.models import ContentType
from surveys.models import Form, Process
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    message = f"{user.full_name} is logged in with ip:{get_client_ip(request)}"
    UserActivity.objects.create(user=user, action_type=LOGIN, remarks=message)


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    message = f"Login Attempt Failed for number {credentials.get('phone_number')} with ip: {get_client_ip(request)}"
    UserActivity.objects.create(action_type=LOGIN_FAILED, remarks=message)

@receiver(post_save, sender=UserActivity)
def sync_view_count(sender , instance, **kwrgs):
    """
    Use django channels to sync all of our reports view counts.
    """

    if instance.action_type == READ:
        model_class = instance.content_type.model_class()
        model_name = instance.content_type.name
        if model_class in [Form,Process]:
            views = UserActivity.count_api_READ_activities(
                model_name,
                object_id=instance.object_id
                )
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"{model_name}_{instance.object_id}",   #   channel_group_name
                {"type": 'on.view', 'views': views}
            )
