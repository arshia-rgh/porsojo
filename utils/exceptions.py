from django.conf import settings


class PorsojoException(Exception):
    def __init__(self, code, message, status_code):
        self.code = code
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return self.message


class TooManyOtpRequestsException(PorsojoException):
    def __init__(self):
        super().__init__(
            code="TOO_MANY_OTP_REQUESTS",
            message=f"Too many otp tokens sent, please try in {settings.OTP_TOKEN_DELETE_DELAY_TEXT} minutes later.",
            status_code=429,
        )


class KavenegarAPIException(PorsojoException):
    def __init__(self, message):
        super().__init__(
            code="KAVENEGAR_API_ERROR",
            message=message,
            status_code=500,
        )


class KavenegarUnexpectedHTTPException(PorsojoException):
    def __init__(self, message):
        super().__init__(
            code="KAVENEGAR_UNEXPECTED_HTTP_ERROR",
            message=message,
            status_code=500,
        )