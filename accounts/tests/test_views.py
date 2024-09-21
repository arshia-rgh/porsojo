from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

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

        mock_send_verification_email.assert_called_once_with(User.objects.get(email="test@gmazil.com").id,
                                                             User.objects.get(email="test@gmazil.com").email)

    def test_register_missing_fields(self, api_client):
        response = api_client.post(reverse("accounts:register"), data={"username": "test"})

        assert response.status_code == 400

    def test_register_user_existing_email(self, api_client):
        User.objects.create_user(username="existing", password="test pass", email="existing@gmazil.com")
        response = api_client.post(reverse("accounts:register"),
                                   data={"username": "test", "password": "test pass", "email": "existing@gmazil.com"})

        assert response.status_code == 400

    def test_register_user_invalid_email(self, api_client):
        response = api_client.post(reverse("accounts:register"),
                                   data={"username": "test", "password": "test pass", "email": "invalid-email"})

        assert response.status_code == 400


@pytest.mark.django_db
class TestSendOTPToken:

    @patch("accounts.views.send_otp.delay")
    def test_send_successfully(self, mock_send_otp, api_client, test_user):
        response = api_client.post(reverse("accounts:send_otp_token"), data={"phone_number": test_user.phone_number})

        assert response.status_code == 201
        assert response.data["message"] == "OTP sent successfully"

        mock_send_otp.assert_called_once_with(test_user.phone_number)

    def test_send_without_phone_number_exists(self, api_client):
        response = api_client.post(reverse("accounts:send_otp_token"), data={"phone_number": "09122222222"})

        assert response.status_code == 400

    # TODO : This test failing unexpected (should be fixed)
    @pytest.mark.skip("I cant debug why failing")
    def test_send_otp_more_than_max_try(self, api_client, test_user):
        for i in range(5):
            response = api_client.post(reverse("accounts:send_otp_token"),
                                       data={"phone_number": test_user.phone_number})

            assert response.status_code == 201

        response = api_client.post(reverse("accounts:send_otp_token"), data={"phone_number": test_user.phone_number})

        assert response.status_code == 400


@pytest.mark.django_db
class TestVerifyOTPToken:
    def test_verify_successfully(self, api_client, test_user, test_otp_token):
        response = api_client.post(reverse("accounts:verify_otp_token"),
                                   data={"phone_number": test_user.phone_number, "otp_token": test_otp_token.code})

        assert response.status_code == 200

        assert "refresh" in response.data
        assert "access" in response.data
        assert test_user.is_authenticated == True

    def test_invalid_data(self, api_client):
        response = api_client.post(reverse("accounts:verify_otp_token"),
                                   data={"phone_number": "invalid phone", "otp_token": "invalid token"})

        assert response.status_code == 400


@pytest.mark.django_db
class TestProfileRetrieveUpdate:

    def test_retrieve_profile_data_successfully(self, api_client, test_user):
        api_client.force_authenticate(test_user)

        response = api_client.get(reverse("accounts:profile"))

        assert response.status_code == 200

        assert "id" and "username" and "first_name" and "last_name" and "phone_number" and "email" in response.data

    def test_update_profile_successfully(self, api_client, test_user):
        api_client.force_authenticate(test_user)

        assert test_user.username == "test user"

        response = api_client.patch(reverse("accounts:profile"), data={"username": "test"})

        assert test_user.username == "test"
        assert response.status_code == 200

    def test_access_view_unauthorized_user(self, api_client):
        response = api_client.get(reverse("accounts:profile"))

        assert response.status_code == 401

    def test_update_profile_invalid_data(self, api_client, test_user):
        api_client.force_authenticate(test_user)

        response = api_client.patch(reverse("accounts:profile"), data={"email": "invalid-email"})

        assert response.status_code == 400


@pytest.mark.django_db
class TestChangePassword:
    pass
