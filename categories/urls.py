from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import FolderViewSet

router = DefaultRouter()
router.register('folders', FolderViewSet)

urlpatterns = [
    path('', include(router.urls))
]
