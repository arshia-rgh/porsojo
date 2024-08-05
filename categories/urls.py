from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import FolderViewSet, FolderItemViewSet

router = DefaultRouter()
router.register('folders', FolderViewSet)
router.register('folder-items', FolderItemViewSet)

urlpatterns = [
    path('', include(router.urls))
]
