from django.urls import path
from rest_framework.routers import DefaultRouter

from analytics.views import UserActivityReadOnlyViewSet

router = DefaultRouter()
router.register(r"activities", UserActivityReadOnlyViewSet, basename="activities")

app_name = "analytics"

urlpatterns = [

] 

urlpatterns += router.urls