from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


from .models import Folder
from .serializers import FolderSerializer


class FolderList(ListCreateAPIView):
    """
    Implements POST method for `Folder` class using `ListCreateAPIView`
    from django rest-framework. It can also retrieves all Folder's objects.

    """

    serializer_class = FolderSerializer
    queryset = Folder.objects.select_related('user').all()


class FolderDetail(RetrieveUpdateDestroyAPIView):
    """
    Implements DELETE, UPDATE, GET methods for a specific `Folder` object using `RetrieveUpdateDestroyAPIView`
    from django rest-framework.

    """
        
    serializer_class = FolderSerializer
    queryset = Folder.objects.select_related('user').all()

