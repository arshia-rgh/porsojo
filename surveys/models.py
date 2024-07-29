from django.db import models

from accounts.models import User


class Form(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
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
    pass


class Answer(models.Model):
    pass


class ProcessForm(models.Model):
    pass


class Response(models.Model):
    pass


class Process(models.Model):
    pass
