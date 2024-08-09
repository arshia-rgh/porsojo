from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ReadOnlyModelViewSet

from surveys.mixins import CachedListMixin
from .models.activities import UserActivity
from .serializers import UserActivitySerializer


class UserActivityReadOnlyViewSet(CachedListMixin, ReadOnlyModelViewSet):
    """
    a ViewSet for UserActivity Model (Read Only)
    """

    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [IsAdminUser]
    cache_key = "activity_list"
