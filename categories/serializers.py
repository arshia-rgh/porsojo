from rest_framework import serializers

from .models import Folder


class FolderSerializer(serializers.ModelSerializer):
    """
    serializer class for `Form` model.
    It uses `Folder` class as its model and all of its fields as well.
    """

    class Meta:
        model = Folder
        fields = ['user', 'name', 'description']