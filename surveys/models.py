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

        if self.is_public:
            self.password = ''

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
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=True)
    password = models.CharField(max_length=100, blank=True)
    is_linear = models.BooleanField()

    def save(self, *args, **kwargs):

        if self.is_public:
            self.password = ''

        elif not self.is_public and self.password == '':
            raise ValueError("Password cannot be empty for non-public processes")
        super().save(*args, **kwargs)


class ProcessForm(models.Model):
    process = models.OneToOneField(Process, on_delete=models.CASCADE)
    # form id

# class Answer(models.Model):
#     pass
#
#

# class Response(models.Model):
#     pass
#
#
