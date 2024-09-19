import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from unittest.mock import patch

User = get_user_model()


@pytest.mark.django_db
class TestUserRegister:
    @patch("accounts.views.send_verification_email.delay")
    def test_register_new_user_successfully(self, mock_send_verification_email, api_client):
        response = api_client.post(reverse("accounts:register"),
                                   data={"username": "test", "password": "test pass", "email": "test@gmazil.com"})

        assert response.status_code == 201
        assert User.objects.get(email="test@gmazil.com") is not None

        assert User.objects.get(email="test@gmazil.com").is_email_verified == False

        mock_send_verification_email.assert_called_once_with(User.objects.get(email="test@gmazil.com").id, User.objects.get(email="test@gmazil.com").email)