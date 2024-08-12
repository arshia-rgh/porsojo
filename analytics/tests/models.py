from django.test import TestCase
from model_bakery import baker

from surveys.models import Form
from analytics.models.activities import UserActivity
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from analytics.constants import *

User = get_user_model()


class UserActivityTest(TestCase):

    def setUp(self):
        self.userali = User.objects.create(username="ali", password="A123456789@", email="ali@gmail.com")
        self.userreza = User.objects.create(username="reza", password="R123456789@", email="reza@gmail.com")
        self.form1 = Form.objects.create(title="form1", user=self.userali)
        self.c_f = ContentType.objects.get_for_model(model=Form)
        self.activitiyRead = baker.make(
            UserActivity,
            user=self.userali,
            action_type=READ,
            status=SUCCESS,
            content_type=self.c_f,
            object_id=self.form1.pk,
        )
        self.activityCreate = baker.make(
            UserActivity,
            user=self.userreza,
            action_type=CREATE,
            status=FAILED,
            content_type=self.c_f,
            object_id=self.form1.pk,
        )

    def test_useracvtivity_model_save_method(self):

        self.assertEqual(self.activitiyRead.content_type, self.c_f)
        self.assertEqual(self.activitiyRead.content_object, self.form1)
        self.assertEqual(self.activitiyRead.user, self.userali)
        self.assertEqual(self.activitiyRead.status, SUCCESS)
        self.assertEqual(self.activitiyRead.action_type, READ)
        # print("models tested")
        self.assertEqual(self.activityCreate.action_type, CREATE)
        self.assertEqual(self.activityCreate.status, FAILED)
        self.assertEqual(self.activityCreate.content_type, self.c_f)
        self.assertEqual(self.activityCreate.content_object, self.form1)
        self.assertEqual(self.activityCreate.user, self.userreza)
