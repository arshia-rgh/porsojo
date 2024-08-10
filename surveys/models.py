from django.db import models

from accounts.models import User
from analytics.models.activities import UserActivity


class Form(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return f"{self.title} - {self.user}"

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
    class QuestionTextChoices(models.TextChoices):
        Text = ("T", "Text")
        Number = ("N", "Number")
        Check_box = ("CB", "Check box")
        Select = ("S", "Select")

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=255)
    question_type = models.CharField(
        max_length=2,
        choices=QuestionTextChoices.choices,
        default=QuestionTextChoices.Text,
    )
    required = models.BooleanField(default=True)
    options = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.text} - {self.question_type}"

    @property
    def separated_options(self):
        return self.options.split(",")


class Process(models.Model):
    forms = models.ManyToManyField(Form, through="ProcessForm")
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    password = models.CharField(max_length=100, blank=True)
    is_linear = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.title} - {self.user}"

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

    def __str__(self) -> str:
        return f"{self.process} - {self.form}"


class Response(models.Model):
    form = models.ForeignKey(
        Form,
        on_delete=models.CASCADE,
    )
    Process = models.OneToOneField(Process, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user} - {self.form}"


class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()

    def __str__(self) -> str:
        return f"{self.question} - {self.answer_text}"
