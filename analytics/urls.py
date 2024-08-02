from django.urls import path
from rest_framework.routers import DefaultRouter

from analytics.views import UserActivityReadOnlyViewSet, ReportViewSet

router = DefaultRouter()
router.register(r"activities", UserActivityReadOnlyViewSet, basename="log")
router.register(r"reports", ReportViewSet, basename="reports")

app_name = "analytics"

urlpatterns = router.urls