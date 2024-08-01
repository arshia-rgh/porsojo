from celery import shared_task
from django.conf import settings

from accounts.models.otp_token import OtpToken
from utils.otp_service import FakeOtpService, KavenegarOtpService


@shared_task
def send_otp(phone_number: str) -> None:
    """
    Sends an OTP token to the provided phone number asynchronously.

    Args:
        phone_number (str): The phone number to send the OTP token to.

    Returns:
        None
    """
    otp_service = FakeOtpService() if settings.DEBUG else KavenegarOtpService(settings.KAVENEGAR_API_TOKEN)
    otp_service.send_otp(phone_number)


@shared_task
def delete_otp_token(otp_token_id: int) -> None:
    """
    Deletes the given OTP token asynchronously.

    Args:
        otp_token_id (int): The ID of the OTP token to delete.

    Returns:
        None
    """
    OtpToken.objects.filter(id=otp_token_id).delete()
