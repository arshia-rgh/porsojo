from django.test import TestCase
from surveys.models import Form, Process, ProcessForm
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


class ProcessModelTest(TestCase):
    def setUp(self):
        self.process1 = baker.make(Process, password='default_password', is_public=True)
        self.form1 = baker.make(Form, is_public=True)
        self.form2 = baker.make(Form, password="test", is_public=False)

    def test_process_model_save_method_with_private_form(self):

        # Create ProcessForm instances to link forms to the process
        ProcessForm.objects.create(process=self.process1, form=self.form1, priority_number=1)
        ProcessForm.objects.create(process=self.process1, form=self.form2, priority_number=2)

        # the process password should not be empty while it is private
        self.process1.password = 'test'
        # Save the process to trigger the save method logic
        self.process1.save()

        # Test if the process is private because it contains a private form
        self.assertEqual(self.process1.is_public, False)
