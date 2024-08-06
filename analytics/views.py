from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models.activities import UserActivity
from .serializers import UserActivitySerializer


class UserActivityReadOnlyViewSet(ReadOnlyModelViewSet):
    """
    a ViewSet for UserActivity Model (Read Only)
    """

    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [IsAdminUser]
