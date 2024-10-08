from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle


class CachedListMixin:
    """
    A cache mixin for handling all viewsets cacheing on the list method
    """

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


class ThrottleMixin:
    """
    A throttle mixin for throttling all viewsets bt 2 scope (upload and receives)
    """

    def get_throttles(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            self.throttle_scope = "uploads"
        else:
            self.throttle_scope = "receives"
        return [ScopedRateThrottle()]
    


class CheckFormPasswordMixin:
    """
    A mixin for checking if the form password is correct
    """

    def password_validation(self, password):
        if not self.get_object().is_public and self.get_object().password != password:
            raise self.serializers.ValidationError({"password": "Incorrect password or form is not public"})

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["password"] = self.request.data.get("password")
        self.password_validation(self.request.data.get("password"))
        return context
    

class CheckProcessPasswordMixin:
    """
    A mixin for checking if the process password is correct
    """

    def password_validation(self, password):
        if not self.get_object().is_public and self.get_object().password != password:
            raise self.serializers.ValidationError({"password": "Incorrect password or process is not public"})

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["password"] = self.request.data.get("password")
        self.password_validation(self.request.data.get("password"))
        return context