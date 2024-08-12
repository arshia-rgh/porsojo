from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient, APITestCase

from accounts.models import User
from analytics.models.activities import UserActivity
from surveys.models import Form


class UserActivityReadOnlyViewSetTest(APITestCase):

    view_name = "activities"
    model = UserActivity

    def setUp(self):
        self.client = APIClient()
        self.user1 = baker.make(User, username="admin", password="admin", is_staff=True)
        # content_type = ContentType.objects.get_for_model(model=Form)

        self.client.force_authenticate(self.user1)
        self.instance1 = baker.make(self.model, user=self.user1)
        self.instance2 = baker.make(self.model, user=self.user1)

    def test_get_with_pk(self):
        response = self.client.get(reverse(f"analytics:{self.view_name}-detail", kwargs={"pk": self.instance1.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

    def test_get_list(self):

        response = self.client.get(reverse(f"analytics:{self.view_name}-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(len(response.json()), 2)

    def test_list_cache(self):
        response = self.client.get(reverse(f"analytics:{self.view_name}-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(len(response.json()), 2)

        # check if cache populated
        cache_key = f"{self.view_name}_list"
        cached_response = cache.get(cache_key)
        # self.assertIsNotNone(cached_response)

        response = self.client.get(reverse(f"analytics:{self.view_name}-list"))
        # self.assertEqual(response.status_code, 200)
        # self.assertEqual(response["Content-Type"], "application/json")
        # self.assertEqual(len(response.json()), 2)
