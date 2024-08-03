from rest_framework import serializers

from .models import Folder


class FormSerializer(serializers.ModelSerializer):
    """
    serializer class for `Form` model.

    """

    class Meta:
        model = Folder
        fields = ['user', 'name', 'description']