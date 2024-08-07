from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ReadOnlyModelViewSet

from surveys.models import Form, Process, Response

from .mixins import UserActivityMixin
from .models.activities import UserActivity
from .serializers import UserActivitySerializer


class UserActivityReadOnlyViewSet(UserActivityMixin, ReadOnlyModelViewSet):
    """
    a ViewSet for UserActivity Model (Read Only)
    """

    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [IsAdminUser]


class ReportDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "report/dashboard.html"
    login_url = "accounts:login_with_username_and_email"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
