from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from .models import Form, ProcessForm, Process
from .serializers import FormSerializer, ProcessFormSerializer, ProcessSerializer


class FormViewSet(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # override the get_throttle() method to add scope for each request methods
    def get_throttles(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            self.throttle_scope = "uploads"
        else:
            self.throttle_scope = "forms"
        return [ScopedRateThrottle()]

    # Cacheing the list method (getting all objects)
    def list(self, request, *args, **kwargs):
        cache_key = 'form_list'
        cached_queryset = cache.get(cache_key)

        if not cached_queryset:
            cached_queryset = list(self.queryset)
            cache.set(cache_key, cached_queryset, 60 * 15)  # Cache for 15 minutes

        serializer = self.get_serializer(cached_queryset, many=True)
        return Response(serializer.data)


class ProcessFormViewSet(viewsets.ModelViewSet):
    queryset = ProcessForm.objects.all()
    serializer_class = ProcessFormSerializer
    permission_classes = [IsAuthenticated]

    def get_throttles(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            self.throttle_scope = "uploads"
        else:
            self.throttle_scope = "forms"
        return [ScopedRateThrottle()]

    # Cacheing the list method (getting all objects)
    def list(self, request, *args, **kwargs):
        cache_key = 'process_form_list'
        cached_queryset = cache.get(cache_key)

        if not cached_queryset:
            cached_queryset = list(self.queryset)
            cache.set(cache_key, cached_queryset, 60 * 15)  # Cache for 15 minutes

        serializer = self.get_serializer(cached_queryset, many=True)
        return Response(serializer.data)


class ProcessViewSet(viewsets.ModelViewSet):
    pass
