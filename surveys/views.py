from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from analytics.mixins import UserActivityMixin
from .mixins import CachedListMixin, ThrottleMixin
from .models import Form, ProcessForm, Process
from .serializers import FormSerializer, ProcessFormSerializer, ProcessSerializer


class FormViewSet(UserActivityMixin,CachedListMixin, ThrottleMixin, viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    cache_key = "form_list"

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    # ensure the view passes the request to the serializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class ProcessFormViewSet(CachedListMixin, ThrottleMixin, viewsets.ModelViewSet):
    queryset = ProcessForm.objects.all()
    serializer_class = ProcessFormSerializer
    permission_classes = [IsAuthenticated]
    cache_key = "process_form_list"


class ProcessViewSet(UserActivityMixin, CachedListMixin, ThrottleMixin, viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    permission_classes = [IsAuthenticated]
    cache_key = "process_list"

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        
    # ensure the view passes the request to the serializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
