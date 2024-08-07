from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from analytics.mixins import UserActivityMixin
from .models import Form
from .serializers import FormSerializer


class FormViewSet(UserActivityMixin, viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Cacheing the list method (getting all objects)
    def list(self, request, *args, **kwargs):
        cache_key = "form_list"
        cached_queryset = cache.get(cache_key)

        if not cached_queryset:
            cached_queryset = list(self.queryset)
            cache.set(cache_key, cached_queryset, 60 * 15)  # Cache for 15 minutes

        serializer = self.get_serializer(cached_queryset, many=True)
        return Response(serializer.data)
