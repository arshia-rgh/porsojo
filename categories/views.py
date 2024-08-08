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
    # permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        user = self.request.user
        print('\n\n', user, '\n\n')
        return {
            'user_id': user
        }


class FolderItemViewSet(ModelViewSet):
    """
    Implements CURD methods for `FolderItem` class using `ModelViewSet`
    from django rest-framework.

    """

    serializer_class = FolderItemSerializer
    queryset = FolderItem.objects.all()
    permission_classes = [IsAuthenticated]
