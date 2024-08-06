from rest_framework import serializers

from .models import Form, ProcessForm, Process


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = '__all__'
        read_only_fields = ['user']

    # set user to the current user
    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['user'] = request.user
        return super().create(validated_data)


class ProcessFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessForm
        fields = "__all__"


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = "__all__"
        read_only_fields = ['user']

    # set user to the current user
    def create(self, validated_data):
        request = self.context.get("request")
        validated_data['user'] = request.user
        return super().create(validated_data)
