from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FormViewSet

router = DefaultRouter()
router.register("forms", FormViewSet)

app_name = "surveys"

urlpatterns = [
    path("", include(router.urls)),
]
