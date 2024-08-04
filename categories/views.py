from rest_framework.viewsets import ModelViewSet

from .models import Folder, FolderItem
from .serializers import FolderSerializer, FolderItemSerializer


class FolderViewSet(ModelViewSet):
    """
    Implements CURD methods for `Folder` class using `ModelViewSet`
    from django rest-framework.

    """

    serializer_class = FolderSerializer
    queryset = Folder.objects.select_related('user').all()


class FolderItemViewSet(ModelViewSet):
    """
    Implements CURD methods for `FolderItem` class using `ModelViewSet`
    from django rest-framework.

    """

    serializer_class = FolderItemSerializer
    queryset = FolderItem.objects.all()
        
