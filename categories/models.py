from django.db import models

from accounts.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Folder(models.Model):
    """
        The `Folder` model is resposible for the different categories in which user creates.

        user: [required] forign key to custom user.  
        name: [required] the title or name of the Folder.  
        description: [optional] brief description of what the `Folder` does.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)


class FolderItem(models.Model):
    """
        The `FolderItem` handles relations between different ContentType's models and `Folder` model.

        folder: represents a Folder model
        content_type: the dynamic model which is stored in ContentType
        object_id: the id of the corrisponding object
        content_object: a generic foreign key which connects content_type & object_id

        More info: https://docs.djangoproject.com/en/5.0/ref/contrib/contenttypes/
    """
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': ('form', 'process')})
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')