from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from analytics.mixins import UserActivityMixin

from .mixins import CachedListMixin, ThrottleMixin
from .models import Form, FormResponse, Process, ProcessForm, ProcessResponse, Question
from .serializers import (
    AnswerSerializer,
    FormPasswordSerializer,
    FormResponseSerializer,
    FormSerializer,
    FormTemplateSerializer,
    ProcessFormSerializer,
    ProcessPasswordSerializer,
    ProcessResponseSerializer,
    ProcessSerializer,
    ProcessTemplateSerializer,
    QuestionSerializer,
    ReceiveProcessResponseSerializer,
    ReceiveSingleFormResponseSerializer,
    SingleFormTemplateSerializer,
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


class ResponseViewSet(UserActivityMixin, CachedListMixin, viewsets.ModelViewSet):
    """
    Implements CURD methods for `Response` class using `ModelViewSet`
    from django rest-framework.
    """

    serializer_class = ResponseSerializer
    queryset = Response.objects.all()
    permission_classes = [IsAuthenticated]
    cache_key = "response_list"

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class QuestionViewSet(UserActivityMixin, CachedListMixin, ThrottleMixin, viewsets.ModelViewSet):
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
        serializer = SingleFormTemplateSerializer(instance=self.get_object())
        return Response(serializer.data)


class ReceiveProcessResponseView(UserActivityMixin, generics.GenericAPIView):
    serializer_class = ReceiveProcessResponseSerializer
    authentication_classes = ()

    def get_process_all_forms(self, process_id):
        queryset = ProcessForm.objects.filter(process__id=process_id).select_related("form").order_by("priority_number")
        return queryset

    def check_forms_has_response(self, forms: list, process_response: ProcessResponse) -> bool:
        return all(
            FormResponse.objects.filter(process_response=process_response, form__id=form).exists() for form in forms
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        process_id = serializer.validated_data["process_id"]
        process_response_id = serializer.validated_data.get("process_response_id")
        priority_number = serializer.validated_data["priority_number"]
        process = get_object_or_404(Process, id=process_id)
        process_response_create = ProcessResponse.objects.get_or_create(
            id=process_response_id,
            defaults={
                "process": process,
                "user": request.user if request.user.is_authenticated else None,
            },
        )
        process_response = process_response_create[0]

        if process.is_linear:
            process_forms = self.get_process_all_forms(process_id)
            less_priority_forms = list(
                process_forms.filter(priority_number__lt=priority_number).values_list("form_id", flat=True)
            )
            if len(less_priority_forms) > 0 and not self.check_forms_has_response(
                less_priority_forms, process_response
            ):
                process_response.delete()
                return Response(
                    {"error": "Higher priority forms must have responses"}, status=status.HTTP_400_BAD_REQUEST
                )

            response_form = process_forms.filter(priority_number=priority_number).first().form

            with transaction.atomic():

                response = FormResponse.objects.create(
                    process_response=process_response,
                    form=response_form,
                    user=request.user if request.user.is_authenticated else None,
                )

                answers_data = serializer.validated_data["answers"]
                for answer_data in answers_data:
                    answer_serializer = AnswerSerializer(data=answer_data)
                    answer_serializer.is_valid(form=response_form, raise_exception=True)
                    answer_serializer.save(commit=False)

                form_response_serializer = FormResponseSerializer(instance=response)
                process_response_serializer = ProcessResponseSerializer(instance=process_response)

            return Response(
                {
                    "message": "Response created successfully",
                    "notice": "Use this process_response_id for submission other forms in this process",
                    "process_response": process_response_serializer.data,
                    "form_response": form_response_serializer.data,
                }
            )

        response_form = ProcessForm.objects.filter(process=process, priority_number=priority_number).first().form
        with transaction.atomic():
            process_response_create = ProcessResponse.objects.get_or_create(
                id=process_response_id,
                defaults={
                    "process": process,
                    "user": request.user if request.user.is_authenticated else None,
                },
            )
            process_response = process_response_create[0]
            response = FormResponse.objects.create(
                process_response=process_response,
                form=response_form,
                user=request.user if request.user.is_authenticated else None,
            )
            answers_data = serializer.validated_data["answers"]
            for answer_data in answers_data:
                answer_serializer = AnswerSerializer(data=answer_data)
                answer_serializer.is_valid(form=response_form, raise_exception=True)
                answer_serializer.save(response=response)

            form_response_serializer = FormResponseSerializer(instance=response)
            process_response_serializer = ProcessResponseSerializer(instance=process_response)

        return Response(
            {
                "message": "Response created successfully",
                "notice": "Use this process_response_id for submission other forms in this process",
                "process_response": process_response_serializer.data,
                "form_response": form_response_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class ReceiveSingleFormResponseView(UserActivityMixin, generics.GenericAPIView):
    serializer_class = ReceiveSingleFormResponseSerializer
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        form = get_object_or_404(Form, pk=serializer.validated_data["form_id"])
        if not form.is_single:
            return Response({"error": "Form is not single, try with process"}, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            response = FormResponse.objects.create(
                form=form,
                user=request.user if request.user.is_authenticated else None,
            )
            answers_data = serializer.validated_data["answers"]
            for answer_data in answers_data:
                answer_serializer = AnswerSerializer(data=answer_data)
                answer_serializer.is_valid(form=form, raise_exception=True)
                answer_serializer.save(response=response)

        form_response_serializer = FormResponseSerializer(instance=response)
        return Response(
            {
                "message": "Response created successfully",
                "form_response": form_response_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
