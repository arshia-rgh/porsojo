from rest_framework import serializers

from analytics.models.activities import UserActivity
from analytics.models.report import Report


class UserActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for UserActivity Model instances
    """
    class Meta:
        model = UserActivity
        fields = [
            "user",
            "action_type",
            "action_time",
            "remarks",
            "status",
        ]


class ReportSerializer(serializers.ModelSerializer):
    """
    A serializer to represent a report in an APIView
    """

    class Meta:
        model = Report
        fields = [
            "content_type",
            "object_id",
            "generated_at",
        ]
