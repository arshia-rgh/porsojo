from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from analytics.mixins import UserActivityMixin

from .mixins import CachedListMixin, ThrottleMixin
from .models import Form, Process, ProcessForm, Question
from .serializers import (
    FormPasswordSerializer,
    FormSerializer,
    FormTemplateSerializer,
    ProcessFormSerializer,
    ProcessPasswordSerializer,
    ProcessSerializer,
    ProcessTemplateSerializer,
    QuestionSerializer,
)


class FormViewSet(CachedListMixin, ThrottleMixin, UserActivityMixin, viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    cache_key = "form_list"

    # ensure the view passes the request to the serializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class ProcessFormViewSet(CachedListMixin, ThrottleMixin, UserActivityMixin, viewsets.ModelViewSet):
    queryset = ProcessForm.objects.all()
    serializer_class = ProcessFormSerializer
    permission_classes = [IsAuthenticated]
    cache_key = "processform_list"


class ProcessViewSet(CachedListMixin, ThrottleMixin, UserActivityMixin, viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    permission_classes = [IsAuthenticated]
    cache_key = "process_list"

    # ensure the view passes the request to the serializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class QuestionViewSet(CachedListMixin, ThrottleMixin, viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    cache_key = "question_list"


class SendProccessTemplateView(UserActivityMixin, generics.GenericAPIView):
    queryset = Process.objects.all()
    serializer_class = ProcessPasswordSerializer
    authentication_classes = ()

    def get_object(self):
        return self.queryset.get(pk=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        if not self.get_object().is_public:
            password_serializer = self.get_serializer(data=request.data, instance=self.get_object())
            password_serializer.is_valid(raise_exception=True)
        serializer = ProcessTemplateSerializer(instance=self.get_object())
        return Response(serializer.data)


class SendFormTemplateView(UserActivityMixin, generics.GenericAPIView):
    queryset = Form.objects.all()
    serializer_class = FormPasswordSerializer
    authentication_classes = ()

    def get_object(self):
        return self.queryset.get(pk=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        if not self.get_object().is_public:
            password_serializer = self.get_serializer(data=request.data, instance=self.get_object())
            password_serializer.is_valid(raise_exception=True)
        serializer = FormTemplateSerializer(instance=self.get_object())
        return Response(serializer.data)
