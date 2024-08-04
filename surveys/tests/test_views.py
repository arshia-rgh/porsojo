from rest_framework.test import APITestCase
from model_bakery import baker
from surveys.models import Form
from django.urls import reverse


class FormViewSetTest(APITestCase):
    def setUp(self):
        self.form1 = baker.make(Form)

    def test_get_with_pk(self):
        response = self.client.get(reverse("surveys:form-detail", kwargs={"pk": self.form1.pk}))
        self.assertEqual(response.status_code, 200)
