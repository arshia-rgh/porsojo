import random

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.validators import iranian_phone_number_validator


class OtpToken(models.Model):
    """This model represent token for otp authentication

    Fields:
        phone_number (CharField)
        code (PositiveSmallIntegerField)
        created (DateTimeField)

    Methods:
        is_expire: if code expired return `True`
        generate_code: generate random 4 digit code
    """

    phone_number = models.CharField(
        _("phone number"),
        max_length=13,
        validators=[iranian_phone_number_validator],
    )
    code = models.PositiveSmallIntegerField(_("code"))
    created = models.DateTimeField(_("created"), auto_now=True)

    def __str__(self):
        return f"{self.phone_number} - {self.code} - {self.created}"

    @property
    def is_expire(self):
        expired = self.created + settings.OTP_EXPIRE
        now = timezone.now()
        if now > expired:
            return True
        return False

    @staticmethod
    def generate_code():
        code = random.randint(1000, 9999)
        return code
