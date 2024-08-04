from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import FormViewSet, ProcessFormViewSet, ProcessViewSet

router = DefaultRouter()
router.register("forms", FormViewSet)
router.register("process-forms", ProcessFormViewSet)
router.register("processes", ProcessViewSet)
app_name = "surveys"

urlpatterns = [
    path("", include(router.urls)),
]
