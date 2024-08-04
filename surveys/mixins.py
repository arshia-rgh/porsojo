from django.core.cache import cache
from rest_framework.response import Response


class CachedListMixin:
    cache_key = None
    cache_timeout = 60 * 15

    def list(self, request, *args, **kwargs):
        if not self.cache_key:
            raise ValueError("cache_key must be set in the viewset")

        cached_queryset = cache.get(self.cache_key)

        if not cached_queryset:
            cached_queryset = list(self.queryset)
            cache.set(self.cache_key, cached_queryset, self.cache_timeout)

        serializer = self.get_serializer(cached_queryset, many=True)
        return Response(serializer.data)
