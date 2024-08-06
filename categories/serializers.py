from rest_framework import serializers


from .models import Folder, FolderItem


class FolderSerializer(serializers.ModelSerializer):
    """
    serializer class for `Form` model.
    It uses `Folder` class as its model and all of its fields as well.
    """

    class Meta:
        model = Folder
        fields = ['id', 'user', 'name', 'description']
        read_only_fields = ['user']

        def create(self, validated_data):
            user_id = self.context['user_id']
            return Folder.objects.create(user_id = user_id, **validated_data)


class FolderItemSerializer(serializers.ModelSerializer):
    """
    serializer class for `FormItem` model.
    It uses `FolderItem` class as its model and all of its fields as well.
    """

    class Meta:
        model = FolderItem
        fields = ['id', 'folder', 'content_type', 'object_id']
