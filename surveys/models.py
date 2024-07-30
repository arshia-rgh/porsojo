from django.db import models

from accounts.models import User


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
            self.password = ''

        # if the form is private and the password is empty should raise an exception
        elif not self.is_public and self.password == '':
            raise ValueError("Password cannot be empty for non-public forms")
        super().save(*args, **kwargs)


class Question(models.Model):
    form = models.ForeignKey(Form, models.CASCADE)
    text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=100)
    required = models.BooleanField(default=True)
    options = models.TextField()


class Process(models.Model):
    forms = models.ManyToManyField(Form, through='ProcessForm')
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    password = models.CharField(max_length=100, blank=True)
    is_linear = models.BooleanField()

    def save(self, *args, **kwargs):
        # If our process contains any private form the process should be private too
        for form in self.forms.all():
            if not form.is_public:
                self.is_public = False

        # if the process is public set the password to empty string
        if self.is_public:
            self.password = ''

        # if the process is private and the password is empty should raise an exception
        elif not self.is_public and self.password == '':
            raise ValueError("Password cannot be empty for non-public processes")
        super().save(*args, **kwargs)


class ProcessForm(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    priority_number = models.IntegerField()


class Response(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    Process = models.OneToOneField(Process, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now=True)


class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
