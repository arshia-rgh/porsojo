from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.validators import iranian_phone_number_validator


class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """

    email = models.EmailField(
        _("email address"),
        blank=True,
        null=True,
        unique=True,
    )

    phone_number = models.CharField(
        _("phone number"),
        max_length=13,
        unique=True,
        null=True,
        blank=True,
        validators=[iranian_phone_number_validator],
    )

    is_email_verified = models.BooleanField(default=False)
