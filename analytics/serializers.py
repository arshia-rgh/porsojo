from rest_framework import serializers

from analytics.models.activities import UserActivity


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
