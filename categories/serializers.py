from rest_framework import serializers

from .models import Folder, FolderItem


class FolderSerializer(serializers.ModelSerializer):
    """
    serializer class for `Form` model.
    It uses `Folder` class as its model and all of its fields as well.
    """

    class Meta:
        model = Folder
        fields = ["id", "user", "name", "description"]


class FolderItemSerializer(serializers.ModelSerializer):
    """
    serializer class for `FormItem` model.
    It uses `FolderItem` class as its model and all of its fields as well.
    """

    class Meta:
        model = FolderItem
        fields = ["id", "folder", "content_type", "object_id"]
