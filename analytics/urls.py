from django.urls import path
from rest_framework.routers import DefaultRouter

from analytics.views import (ReportDashboardView, ReportFormView,
                             ReportProcessView, UserActivityReadOnlyViewSet)

router = DefaultRouter()
router.register(r"activities", UserActivityReadOnlyViewSet, basename="activities")

app_name = "analytics"

urlpatterns = [
    path("reports/", ReportDashboardView.as_view(), name="reports"),
    path("report/form/<int:pk>/", ReportFormView.as_view(), name="report_form"),
    path("report/process/<int:pk>/",ReportProcessView.as_view(),name="report_process"),
]

urlpatterns += router.urls
