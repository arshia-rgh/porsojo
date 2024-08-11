from rest_framework import serializers

from .models import Answer, Answer, Form, Process, ProcessForm, Question


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

    class Meta:
        model = Form
        fields = ("id", "title", "description", "questions", "priority_number")

    def get_priority_number(self, obj):
        """
        Returns the priority number of the form in its process.
        """
        process_form = ProcessForm.objects.get(form=obj)
        return process_form.priority_number


class ProcessTemplateSerializer(serializers.ModelSerializer):
    forms = FormTemplateSerializer(many=True)

    class Meta:
        model = Process
        fields = ("id", "title", "description", "is_public", "is_linear", "forms")


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