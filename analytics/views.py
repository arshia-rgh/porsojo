from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from analytics.models.report import Report
from analytics.serializers import ReportSerializer

from .models.activities import UserActivity
from .serializers import UserActivitySerializer



class UserActivityReadOnlyViewSet(ReadOnlyModelViewSet):
    """
    a ViewSet for UserActivity Model (Read Only)
    """
    
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer


class ReportViewSet(viewsets.ModelViewSet):
    """
    A generic view for reading reports
    """
    queryset = Report.objects.all()
    serializer_class= ReportSerializer
    permission_classes= [IsAuthenticated]


