from unittest import skip

from django.core.cache import cache
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APITestCase, APIClient

from accounts.models import User
from surveys.models import Form


class FormViewSetTest(APITestCase):
    def setUp(self):
        # clear cache for testing throttle
        cache.clear()

        self.client = APIClient()
        self.user1 = baker.make(User)
        self.client.force_authenticate(user=self.user1)
        self.form1 = baker.make(Form, password="test password")
        self.form2 = baker.make(Form, password="test password2")

    @skip
    def test_throttling(self):
        """
            Test the throttling mechanism for the FormViewSet.

            This test will be skipped. To run this test, ensure the throttle rates are set to 5  in the settings.

            Steps: 1. Send 5 requests to the form-list endpoint and verify each response has a status code of 200. 2.
            Send a 6th request to the form-list endpoint and verify the response has a status code of 429 (Too Many
            Requests).
        """
        for _ in range(5):
            response = self.client.get(reverse("surveys:form-list"))
            self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("surveys:form-list"))
        self.assertEqual(response.status_code, 429)

        for _ in range(5):
            response = self.client.post(reverse("surveys:form-list"), data={
                "title": "Test Form",
                "description": "test description",
                "password": "test password",
                "user": self.user1.id
            })
            self.assertEqual(response.status_code, 201)

        response = self.client.post(reverse("surveys:form-list"), data={
            "title": "Test Form",
            "description": "test description",
            "password": "test password",
            "user": self.user1.id,
        })
        self.assertEqual(response.status_code, 429)

    def test_get_with_pk(self):
        response = self.client.get(reverse("surveys:form-detail", kwargs={"pk": self.form1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_get_list(self):
        response = self.client.get(reverse("surveys:form-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(len(response.json()), 2)

    def test_list_cache(self):
        # First request should populate the cache
        response = self.client.get(reverse("surveys:form-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(len(response.json()), 2)

        # Check if the cache is populated
        cache_key = "form_list"
        cached_response = cache.get(cache_key)
        self.assertIsNotNone(cached_response)

        # Second request should hit the cache
        response = self.client.get(reverse("surveys:form-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(len(response.json()), 2)
