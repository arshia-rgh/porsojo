from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        r"analytics/report/form/(?P<form_id>\d+)/$",
        consumers.ReportFormConsumer.as_asgi(),
    ),
    re_path(
        r"analytics/report/process/(?P<form_id>\d+)/$",
        consumers.ReportProcessConsumer.as_asgi(),
    ),
]
