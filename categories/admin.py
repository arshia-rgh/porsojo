from django.contrib import admin

from .models import Folder, FolderItem

admin.site.register(Folder)
admin.site.register(FolderItem)
