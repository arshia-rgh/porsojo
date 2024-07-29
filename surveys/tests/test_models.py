from django.test import TestCase
from surveys.models import Form
from model_bakery import baker


class FormModelTest(TestCase):
    def setUp(self):
        self.form1 = baker.make(Form, password='default_password', is_public=True)

    def test_form_model_save_method(self):
        # Test if the form is public and has a non-blank password, it will set the password to blank
        self.assertEqual(self.form1.password, '')

        # Test if the form is private and does not have a password, it should raise a ValueError exception
        self.form1.password = ''
        self.form1.is_public = False
        with self.assertRaises(ValueError):
            self.form1.save()
