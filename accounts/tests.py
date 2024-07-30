import json
from unittest.mock import patch

from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models.otp_token import OtpToken
from accounts.models.user import User
from utils.otp_service import FakeOtpService


class AccountsEndpointTestCase(APITestCase):

    def setUp(self) -> None:
        self.user_data = {
            "username": "test",
            "email": "LpV4K@example.com",
            "phone_number": "09123456789",
            "password": "Test@1234",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }

    def create_user(self) -> User:
        return User.objects.create_user(**self.user_data)

    def test_user_registration(self) -> None:
        url = reverse("accounts:register")
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        user_data = self.user_data.copy()
        user_data.pop("password")
        user_data["id"] = 1
        self.assertEqual(response.data, user_data)

    def test_user_login_with_password(self) -> None:
        self.create_user()
        url = reverse("accounts:login_with_username_and_email")
        response = self.client.post(
            url,
            {
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "access")
        self.assertContains(response, "refresh")

    def test_user_login_with_email(self) -> None:
        self.create_user()
        url = reverse("accounts:login_with_username_and_email")
        response = self.client.post(
            url,
            {
                "username": self.user_data["email"],
                "password": self.user_data["password"],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "access")
        self.assertContains(response, "refresh")

    def test_user_login_with_wrong_password_or_username_or_email(self) -> None:
        self.create_user()
        url = reverse("accounts:login_with_username_and_email")
        response = self.client.post(
            url,
            {
                "username": self.user_data["username"],
                "password": "wrong_password",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "No active account found with the given credentials"})

        response = self.client.post(
            url,
            {
                "username": "wrong_username",
                "password": self.user_data["password"],
            },
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "No active account found with the given credentials"})

    @override_settings(DEBUG=True)
    def test_user_send_otp_valid_request(self) -> None:
        self.create_user()
        url = reverse("accounts:send_otp_token")
        response = self.client.post(url, {"phone_number": self.user_data["phone_number"]})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "OTP sent successfully"})

    @override_settings(DEBUG=False)
    def test_user_send_otp_invalid_request(self) -> None:
        url = reverse("accounts:send_otp_token")
        response = self.client.post(url, {"phone_number": "09127548715"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("phone_number" in response.data)

    @override_settings(DEBUG=True)
    def test_verify_otp_token_valid_request(self):
        self.create_user()
        self.client.post(reverse("accounts:send_otp_token"), {"phone_number": self.user_data["phone_number"]})

        url = reverse("accounts:verify_otp_token")
        otp_code = OtpToken.objects.filter(phone_number=self.user_data["phone_number"]).first().code
        response = self.client.post(url, {"phone_number": self.user_data["phone_number"], "otp_token": otp_code})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(DEBUG=True)
    def test_verify_otp_token_invalid_request(self):
        self.create_user()
        self.client.post(reverse("accounts:send_otp_token"), {"phone_number": self.user_data["phone_number"]})

        url = reverse("accounts:verify_otp_token")
        otp_code = OtpToken.objects.filter(phone_number=self.user_data["phone_number"]).first().code
        response = self.client.post(url, {"phone_number": self.user_data["phone_number"], "otp_token": otp_code + 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
