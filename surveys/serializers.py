from rest_framework import serializers

from .models import Form, ProcessForm, Process, Question, Response


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


class ResponseSerializer(serializers.ModelSerializer):
    """
        a serializer class for `Response` model.
    """
    class Meta:
        model = Response
        fields = '__all__'
        read_only_fields = ['user']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"
