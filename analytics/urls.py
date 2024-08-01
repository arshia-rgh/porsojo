from django.urls import path
from rest_framework.routers import DefaultRouter

from analytics.views import ReportAPIView

from .views import UserActivityReadOnlyViewSet

router = DefaultRouter()
router.register(r"", UserActivityReadOnlyViewSet, basename="log")

app_name = "analytics"

urlpatterns = [
    path("report/<int:pk>", ReportAPIView.as_view(), name="report_detail"),
    router.urls
]