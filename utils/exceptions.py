from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class PorsojoException(APIException):
    pass


class TooManyOtpRequestsException(PorsojoException):
    default_detail = _(f"Too many requests. Please try {settings.OTP_TOKEN_DELETE_DELAY_TEXT} min later.")
    default_code = "too_many_requests"
    status_code = status.HTTP_429_TOO_MANY_REQUESTS


class KavenegarAPIException(PorsojoException):
    default_detail = _("Kavenegar API error")
    default_code = "kavenegar_api_error"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class KavenegarUnexpectedHTTPException(PorsojoException):
    default_detail = _("Unexpected HTTP error")
    default_code = "kavenegar_unexpected_http_error"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
