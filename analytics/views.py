from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ReadOnlyModelViewSet

from surveys.models import Form, Process, Response

from .mixins import UserActivityMixin
from surveys.mixins import CachedListMixin
from .models.activities import UserActivity
from .serializers import UserActivitySerializer


class UserActivityReadOnlyViewSet(CachedListMixin, UserActivityMixin, ReadOnlyModelViewSet):
    """
    a ViewSet for UserActivity Model (Read Only)
    """

    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [IsAdminUser]
    cache_key = "activity_list"


class ReportDashboardView(LoginRequiredMixin, TemplateView):
    """
    Reports dashboard holds an endpoints to all form and process reports a user has.
    Except for admin, each User has only access to their own contents' reports.
    """

    template_name = "report/dashboard.html"
    login_url = "accounts:login_with_username_and_email"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.is_admin:
            context["forms"] = Form.objects.all()
            context["processes"] = Process.objects.all()
        else:
            context["forms"] = Form.objects.filter(user=self.request.user)
            context["processes"] = Process.objects.filter(user=self.request.user)
        return context


class ReportFormView(LoginRequiredMixin, DetailView):
    """
    This is a DetailView for form reports. Each form has its own report View.
    """

    template_name = "report/Form_report.html"
    model = Form
    queryset = Form.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["responses"] = Response.objects.filter(form=self.get_object())
        return context


class ReportProcessView(LoginRequiredMixin, DetailView):
    """
    This is a DetailView for process reports. Each process has its own report View.
    """

    template_name = "report/Process_report.html"
    model = Process
    queryset = Process.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["responses"] = Response.objects.filter(process=self.get_object())
        return context
