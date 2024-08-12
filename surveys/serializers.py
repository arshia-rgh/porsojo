from rest_framework import serializers

from .models import (
    Answer,
    Form,
    FormResponse,
    Process,
    ProcessForm,
    ProcessResponse,
    Question,
)


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = "__all__"
        read_only_fields = ["user"]

    # set user to the current user
    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user
        return super().create(validated_data)


class ProcessFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessForm
        fields = "__all__"


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = "__all__"
        read_only_fields = ["user"]

    # set user to the current user
    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user
        return super().create(validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class QuestionResponseSerializer(serializers.ModelSerializer):
    question_type = serializers.CharField(source="get_question_type_display")

    class Meta:
        model = Question
        fields = ("id", "text", "question_type", "options")


class FormTemplateSerializer(serializers.ModelSerializer):
    questions = QuestionResponseSerializer(many=True)
    priority_number = serializers.SerializerMethodField(read_only=True)
    process = serializers.PrimaryKeyRelatedField(queryset=Process.objects.all(), required=False)

    class Meta:
        model = Form
        fields = ("id", "title", "description", "is_public", "is_single", "questions", "priority_number", "process")

    def get_priority_number(self, obj, *args, **kwargs):
        """
        Returns the priority number of the form in its process.
        """
        process = self.context.get("process")
        if not process:
            return None
        process_form = ProcessForm.objects.filter(form=obj, process=process).first()
        return process_form.priority_number


class SingleFormTemplateSerializer(serializers.ModelSerializer):
    questions = QuestionResponseSerializer(many=True)

    class Meta:
        model = Form
        fields = ("id", "title", "description", "is_public", "is_single", "questions")


class ProcessTemplateSerializer(serializers.ModelSerializer):
    forms = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Process
        fields = ("id", "title", "description", "is_public", "is_linear", "forms")

    def get_forms(self, obj, *args, **kwargs):
        self.context["process"] = obj
        return FormTemplateSerializer(obj.forms.all(), many=True, context=self.context).data


class FormPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100)

    class Meta:
        model = Form
        fields = ("password",)

    def validate_password(self, value):
        if not self.instance.is_public and self.instance.password != value:
            raise serializers.ValidationError("Incorrect password")
        return value


class ProcessPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100)

    class Meta:
        model = Process
        fields = ("password",)

    def validate_password(self, value):
        if not self.instance.is_public and self.instance.password != value:
            raise serializers.ValidationError("Incorrect password")
        return value


class ReceiveProcessResponseSerializer(serializers.Serializer):
    process_id = serializers.IntegerField()
    process_response_id = serializers.IntegerField(required=False)
    priority_number = serializers.IntegerField()
    answers = serializers.JSONField()


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("question", "response", "answer_text")
        extra_kwargs = {"response": {"required": False}}

    def is_valid(self, form: Form, raise_exception=False):
        questions = form.questions.all()
        if self.initial_data["question"] not in [question.id for question in questions]:
            raise serializers.ValidationError({"question": "This `question` not belong to this form."})
        return super().is_valid(raise_exception=raise_exception)


class FormResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormResponse
        fields = "__all__"


class ProcessResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessResponse
        fields = "__all__"


class ReceiveSingleFormResponseSerializer(serializers.Serializer):
    form_id = serializers.IntegerField()
    answers = serializers.JSONField()
