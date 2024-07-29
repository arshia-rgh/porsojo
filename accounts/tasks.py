from celery import shared_task

from utils.otp_service import BaseOtpService


@shared_task
def send_otp(otp_service: BaseOtpService, phone_number: str) -> None:
    """
    Asynchronously sends an OTP (One-Time Password) to a given phone number.

    :param otp_service: The OTP service to use for sending the OTP.
    :type otp_service: BaseOtpService
    :param phone_number: The phone number to send the OTP to.
    :type phone_number: str
    :return: None
    """
    otp_service.send_otp(phone_number)
