from django.db import models

from accounts.models import User
from analytics.models.activities import UserActivity


class Form(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):

        # if the form is public set the password to empty string
        if self.is_public:
            self.password = ""

        # if the form is private and the password is empty should raise an exception
        elif not self.is_public and self.password == "":
            raise ValueError("Password cannot be empty for non-public forms")
        super().save(*args, **kwargs)

    @property
    def view_count(self) -> int:
        """
        Counts the number of views for each instance
        """
        return UserActivity.count_api_READ_activities(
            "form",  #   must give model name as str
            self.pk,
        )

    @property
    def response_count(self) -> int:
        """
        return number of responses given to the Process object
        """
        return Response.objects.filter(form=self).count()


class Question(models.Model):
    QUESTION_TYPES = (
        ("Text", "Text"),
        ("Check_box", "Check_box"),
        ("Select", "Select"),
    )
    form = models.ForeignKey(Form, models.CASCADE)
    text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=100, choices=QUESTION_TYPES, default="Text")
    required = models.BooleanField(default=True)
    options = models.TextField()

    @property
    def separated_options(self):
        return self.options.split(",")


class Process(models.Model):
    forms = models.ManyToManyField(Form, through="ProcessForm")
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    password = models.CharField(max_length=100, blank=True)
    is_linear = models.BooleanField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # If our process contains any private form the process should be private too
        contains_private_form = any(not form.is_public for form in self.forms.all())

        if contains_private_form:
            self.is_public = False

        # if the process is public set the password to empty string
        if self.is_public:
            self.password = ""

        # if the process is private and the password is empty should raise an exception
        elif not self.is_public and self.password == "":
            raise ValueError("Password cannot be empty for non-public processes")
        super().save(*args, **kwargs)

    @property
    def view_count(self) -> int:
        """
        Counts the number of views for each instance
        """
        return UserActivity.count_api_READ_activities(
            "Process",  #    must give model name as str
            self.pk,
        )

    @property
    def response_count(self) -> int:
        """
        return number of responses given to the Process object
        """
        fc = ProcessForm.objects.filter(process=self).count()
        resp_count = Response.objects.filter(process=self).count()

        return int(resp_count / fc)  # devide responses per forms


class ProcessForm(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    priority_number = models.IntegerField()


class Response(models.Model):
    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
    )
    process = models.ForeignKey(Process, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now=True)


class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
