from celery import shared_task

from accounts.models.otp_token import OtpToken
from utils.otp_service import BaseOtpService


@shared_task
def send_otp(otp_service: BaseOtpService, phone_number: str) -> None:
    """
    Sends an OTP token to the provided phone number asynchronously.

    Args:
        otp_service (BaseOtpService): The OTP service to use.
        phone_number (str): The phone number to send the OTP token to.

    Returns:
        None
    """

    otp_service.send_otp(phone_number)


@shared_task
def delete_otp_token(otp_token: OtpToken) -> None:
    """
    Deletes the given OTP token asynchronously.

    Args:
        otp_token (OtpToken): The OTP token to delete.

    Returns:
        None
    """

    otp_token.delete()
