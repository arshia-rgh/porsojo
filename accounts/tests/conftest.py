import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from accounts.models.otp_token import OtpToken

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    return User.objects.create_user(
        username="test user",
        password="test pass",
        phone_number="09111111111",
        email="test@gmail.com",
    )


@pytest.fixture
def test_otp_token(test_user):
    return OtpToken.objects.create(phone_number=test_user.phone_number)
