from celery import shared_task
from django.conf import settings
from django.urls import reverse
from accounts.models.otp_token import OtpToken
from utils.otp_service import BaseOtpService, FakeOtpService, KavenegarOtpService
from django.core.mail import send_mail
from utils.email_verification_uid import generate_email_verification_token, generate_uid


def get_otp_service() -> BaseOtpService:
    """
    Returns the OTP service to use.

    Returns:
        BaseOtpService: The OTP service to use.
    """

    if settings.DEBUG:
        return FakeOtpService()
    return KavenegarOtpService(settings.KAVENEGAR_API_TOKEN)


@shared_task
def send_otp(phone_number: str) -> None:
    """
    Sends an OTP token to the provided phone number asynchronously.

    Args:
        otp_service (BaseOtpService): The OTP service to use.
        phone_number (str): The phone number to send the OTP token to.

    Returns:
        None
    """
    otp_service = get_otp_service()
    otp_service.send_otp(phone_number)


@shared_task
def delete_otp_token(otp_token_id: int) -> None:
    """
    Deletes the given OTP token asynchronously.

    Args:
        otp_token (OtpToken): The OTP token to delete.

    Returns:
        None
    """

    OtpToken.objects.filter(id=otp_token_id).first().delete()


@shared_task
def send_verification_email(user_id, email):
    from django.contrib.auth import get_user_model

    User = get_user_model()
    user = User.objects.get(pk=user_id)
    token = generate_email_verification_token(user)
    uid = generate_uid(user)
    # uidb64 and token will be sent as dynamic parts of the URL
    verification_link = (
        f"{settings.FRONTEND_URL}{reverse("accounts:verify_email", kwargs={'uidb64': uid, 'token': token})}"
    )

    subject = "Verify your email address"
    message = f"Please click the link below to verify your email address:\n{verification_link}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
