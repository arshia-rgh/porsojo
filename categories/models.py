from django.db import models


class Folder(models.Model):
    """
        The `Folder` model is resposible for the different categories in which user creates.

        user: forign key to custom user.  
        name: the title or name of the Folder.  
        description: [optional] brief description of what the `Folder` does.
    """

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='folders')
    name = models.CharField()
    description = models.CharField(blank=True)


class FolderItem(models.Model):
    # object_id = 
    folder = models.ForeignKey(Folder, on_delete=models.PROTECT, related_name='items')
    content_id = models.IntegerField()
    