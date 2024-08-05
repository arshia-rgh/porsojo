from celery.contrib.testing.worker import start_worker
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models.user import User
from config.celery import app

from .serializer import ProfileSerializer


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
        start_worker(app=app)

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

    def test_profile_retrieve(self):
        user = self.create_user()
        self.client.force_authenticate(user)
        url = reverse("accounts:profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ProfileSerializer(instance=user).data)

    def test_profile_partial_update(self):
        user = self.create_user()
        self.client.force_authenticate(user)
        url = reverse("accounts:profile")
        response = self.client.patch(url, {"phone_number": "09123456789"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ProfileSerializer(instance=user).data)
