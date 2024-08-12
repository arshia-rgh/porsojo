import json
from types import NoneType

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.db.models.signals import post_save
from django.dispatch import receiver

from analytics.constants import CREATE, LOGIN, LOGIN_FAILED, READ, SUCCESS
from analytics.models.activities import UserActivity
from surveys.models import Form, Process, Response
from utils.client_ip_service import get_client_ip


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    message = f"{user} is logged in with ip:{get_client_ip(request)}"
    UserActivity.objects.create(user=user, action_type=LOGIN, remarks=message)


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    message = f"Login Attempt Failed for number {credentials.get('phone_number')} with ip: {get_client_ip(request)}"
    UserActivity.objects.create(action_type=LOGIN_FAILED, remarks=message)


@receiver(post_save, sender=UserActivity)
def sync_report_details(sender, instance, **kwrgs):
    """
    Use django channels to sync all of our reports details.
    """
    #   we don't want any update on views for activities without any content.
    if type(instance.content_type) is NoneType:
        return

    model_class = instance.content_type.model_class()
    model_name = instance.content_type.name
    channel_layer = get_channel_layer()

    #   Only check successful activites

    successful = True if instance.status == SUCCESS else False

    #   check if anyone has viewed any particular Process or form.
    #   if yes ==> update it in our report channel layer.
    if successful and instance.action_type == READ and (model_class in [Form, Process]) and instance.content_object:
        views = UserActivity.count_api_READ_activities(model_name, object_id=instance.object_id)
        async_to_sync(channel_layer.group_send)(
            f"{model_name}_{instance.object_id}",  #   channel_group_name
            {"type": "on.view", "views": views},
        )

    #   check if any response hase been created
    #   if yes ==> update our responses in report channel layer
    if successful and (instance.action_type == CREATE) and (model_class is Response):
        response = Response.objects.get(instance.object_id)
        response_count = response.process.response_count

        #   async send response_count report
        #   connected to ReportConsumer on_response_count
        async_to_sync(channel_layer.group_send)(
            f"{model_name}_{instance.object_id}",  #   channel_group_name
            {"type": "on.reponse_count", "response_count": response_count},
        )

        #   async send response to report
        #   connected to ReportConsumer on_response
        async_to_sync(channel_layer.group_send)(
            f"{model_name}_{instance.object_id}",  #   channel_group_name
            {"type": "on.reponse", "response": json.dumps(response)},
        )
        
