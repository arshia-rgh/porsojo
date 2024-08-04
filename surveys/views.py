from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .mixins import CachedListMixin, ThrottleMixin
from .models import Form, ProcessForm, Process
from .serializers import FormSerializer, ProcessFormSerializer, ProcessSerializer


class FormViewSet(CachedListMixin, ThrottleMixin, viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    cache_key = "form_list"


class ProcessFormViewSet(CachedListMixin, ThrottleMixin, viewsets.ModelViewSet):
    queryset = ProcessForm.objects.all()
    serializer_class = ProcessFormSerializer
    permission_classes = [IsAuthenticated]
    cache_key = "process_form_list"


class ProcessViewSet(CachedListMixin, ThrottleMixin, viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    permission_classes = [IsAuthenticated]
    cache_key = "process_list"
