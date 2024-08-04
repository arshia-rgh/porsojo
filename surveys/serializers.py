from rest_framework import serializers

from .models import Form, ProcessForm, Process


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = '__all__'


class ProcessFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessForm
        fields = "__all__"


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = "__all__"
