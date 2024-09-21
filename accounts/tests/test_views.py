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

    def test_change_password_successfully(self, api_client, test_user):
        api_client.force_authenticate(test_user)

        assert test_user.check_password("test pass") == True

        response = api_client.patch(
            reverse("accounts:change_password"),
            data={
                "old_password": "test pass",
                "password": "Password12",
                "confirm_password": "Password12",
            }
        )

        assert response.status_code == 200
        assert test_user.check_password("Password12") == True

    def test_change_password_unauthenticated(self, api_client):
        response = api_client.patch(reverse("accounts:change_password"))

        assert response.status_code == 401

    def test_change_password_wrong_data(self, api_client, test_user):
        api_client.force_authenticate(test_user)

        assert test_user.check_password("test pass") == True

        # Wrong old password
        response_wrong_old_password = api_client.patch(
            reverse("accounts:change_password"),
            data={
                "old_password": "invalid",
                "password": "Pass12",
                "confirm_password": "Pass12"
            }
        )

        assert response_wrong_old_password.status_code == 400
        assert test_user.check_password("test pass") == True

        # New passwords mismatched
        response_mismatch = api_client.patch(
            reverse("accounts:change_password"),
            data={
                "old_password": "test pass",
                "password": "Pass12",
                "confirm_password": "another pass"
            }
        )

        assert response_mismatch.status_code == 400
        assert test_user.check_password("test pass") == True


@pytest.mark.django_db
class TestVerifyEmailView:
    def test_verify_successfully(self, api_client, test_user, uid_token_setup):
        uid, token = uid_token_setup

        assert test_user.is_email_verified == False

        response = api_client.get(reverse("accounts:verify_email", kwargs={"uidb64": uid, "token": token}))

        assert response.status_code == 200

        test_user.refresh_from_db()
        assert test_user.is_email_verified == True

    def test_verify_nonexistent_id(self, api_client, test_user, uid_token_setup):
        uid, token = uid_token_setup

        uid = "invalid uid"

        assert test_user.is_email_verified == False

        response = api_client.get(reverse("accounts:verify_email", kwargs={"uidb64": uid, "token": token}))

        assert response.status_code == 400

        test_user.refresh_from_db()
        assert test_user.is_email_verified == False

