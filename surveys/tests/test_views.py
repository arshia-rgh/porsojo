from unittest import skip

from django.core.cache import cache
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APITestCase, APIClient

from accounts.models import User
from surveys.models import Form, ProcessForm, Process


class BaseViewSetTest(APITestCase):
    view_name = None
    model = None

    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.user1 = baker.make(User)
        self.client.force_authenticate(user=self.user1)
        self.instance1 = baker.make(self.model)
        self.instance2 = baker.make(self.model)

    def test_get_with_pk(self):
        response = self.client.get(reverse(f"surveys:{self.view_name}-detail", kwargs={"pk": self.instance1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_get_list(self):
        response = self.client.get(reverse(f"surveys:{self.view_name}-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(len(response.json()), 2)

    def test_post_create(self):
        raise NotImplementedError("test_post_create must be implemented")

    def test_list_cache(self):
        response = self.client.get(reverse(f"surveys:{self.view_name}-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(len(response.json()), 2)

        # check if cache populated
        cache_key = f"{self.view_name}_list"
        cached_response = cache.get(cache_key)
        self.assertIsNotNone(cached_response)

        response = self.client.get(reverse(f"surveys:{self.view_name}-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(len(response.json()), 2)


class FormViewSetTest(BaseViewSetTest):
    view_name = "form"
    model = Form

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
            response = self.client.post(
                reverse("surveys:form-list"),
                data={
                    "title": "Test Form",
                    "description": "test description",
                    "password": "test password",
                },
            )
            self.assertEqual(response.status_code, 201)

        response = self.client.post(
            reverse("surveys:form-list"),
            data={
                "title": "Test Form",
                "description": "test description",
                "password": "test password",
            },
        )
        self.assertEqual(response.status_code, 429)

    def test_post_create(self):
        response = self.client.post(
            reverse("surveys:form-list"),
            data={
                "title": "Test Form  Unique",
                "description": "test description",
                "password": "test password",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Form.objects.get(title="Test Form  Unique").exists())


class ProcessFormViewSetTest(BaseViewSetTest):
    view_name = "processform"
    model = ProcessForm

    def test_post_create(self):
        response = self.client.post(
            reverse("surveys:processform-list"),
            data={"process": baker.make(Process), "form": baker.make(Form), "priority_number": 2},
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(ProcessForm.objects.all().exists())


class ProcessViewSetTest(BaseViewSetTest):
    view_name = "process"
    model = Process

    def test_post_create(self):
        response = self.client.post(
            reverse("surveys:process-list"),
            data={
                "forms": baker.make(Form),
                "title": "Test Title",
                "description": "Test description",
                "is_linear": False,
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Process.objects.all().exists())
