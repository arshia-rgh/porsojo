from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Folder, FolderItem
from .serializers import FolderSerializer, FolderItemSerializer


class FolderViewSet(ModelViewSet):
    """
    Implements CURD methods for `Folder` class using `ModelViewSet`
    from django rest-framework.

    """

    serializer_class = FolderSerializer
    queryset = Folder.objects.select_related('user').all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class FolderItemViewSet(ModelViewSet):
    """
    Implements CURD methods for `FolderItem` class using `ModelViewSet`
    from django rest-framework.

    """

    serializer_class = FolderItemSerializer
    queryset = FolderItem.objects.all()
    permission_classes = [IsAuthenticated]
