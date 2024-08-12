from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        r"analytics/report/(?P<content>\w+)/(?P<id>\d+)/$",
        consumers.ReportConsumer.as_asgi(),
    )
]
