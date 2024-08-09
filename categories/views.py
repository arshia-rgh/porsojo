from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from surveys.mixins import CachedListMixin
from .models import Folder, FolderItem
from .serializers import FolderSerializer, FolderItemSerializer


class FolderViewSet(CachedListMixin, ModelViewSet):
    """
    Implements CURD methods for `Folder` class using `ModelViewSet`
    from django rest-framework.

    """

    serializer_class = FolderSerializer
    queryset = Folder.objects.select_related("user").all()
    permission_classes = [IsAuthenticated]
    cache_key = "folder_list"


class FolderItemViewSet(CachedListMixin, ModelViewSet):
    """
    Implements CURD methods for `FolderItem` class using `ModelViewSet`
    from django rest-framework.

    """

    serializer_class = FolderItemSerializer
    queryset = FolderItem.objects.all()
    permission_classes = [IsAuthenticated]
    cache_key = "folderitem_list"
