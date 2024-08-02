from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from accounts.models.user import User
from analytics.constants import ACTION_STATUS, ACTION_TYPES, SUCCESS


class UserActivity(models.Model):
    """
    Stores a user activity, based on its action_type related to :model:"accounts.User"

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    action_type = models.CharField(max_length=15,choices= ACTION_TYPES)
    action_time =  models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(choices=ACTION_STATUS, max_length=7, default=SUCCESS)
    data = models.JSONField(default=dict)

    # for generic relations
    content_type = models.ForeignKey(
        ContentType, models.SET_NULL, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey()

    def __str__(self) -> str:
        return f"{self.action_type} by {self.user} on {self.action_time}"