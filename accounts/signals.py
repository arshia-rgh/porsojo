from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from accounts.models.otp_token import OtpToken
from accounts.tasks import delete_otp_token


@receiver(post_save, sender=OtpToken)
def schedule_opt_token_deletion(sender, instance, created, **kwargs):
    if created:
        delete_time = timezone.now() + settings.OTP_TOKEN_DELETE_DELAY
        delete_otp_token.apply_async(args=[instance], eta=delete_time)
