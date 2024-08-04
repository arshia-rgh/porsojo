from rest_framework.viewsets import ModelViewSet

from .models import Folder
from .serializers import FolderSerializer


class FolderViewSet(ModelViewSet):
    """
    Implements CURD methods for `Folder` class using `ModelViewSet`
    from django rest-framework.

    """

    serializer_class = FolderSerializer
    queryset = Folder.objects.select_related('user').all()
        
