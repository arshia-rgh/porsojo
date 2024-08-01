from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from surveys.models import Form, Process, ProcessForm, Response

from .activities import UserActivity


class Report(models.Model):
    """
    Report Model represents report entity in db for either a Form or a Process. it indicates visit_count + response_count
    """

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"model__in":("form","process")}
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type","object_id")
    generated_at = models.DateTimeField("date report was generated", auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        verbose_name= "report"
        verbose_name_plural= "reports"
        unique_together = ("content_type", "object_id")
        ordering = ["generated_at"]

    @property
    def view_count(self) -> int:
        """
        returns number of object's views
        """
        views_count = UserActivity.objects.filter(
            content_type=self.content_type,
            object_id=self.object_id,
            action_type = "Read"
        ).count()
        return views_count
        
    @property
    def response_count(self) -> int:
        """
        return number of responses given to the report's object (Form or Process)
        """
        if self.content_type.model_class() is Form:
            return Response.objects.filter(form__id=self.object_id).count()
        
        if self.content_type.model_class() is Process:
            forms_count=ProcessForm.objects.filter(process__id=self.object_id).count()
            #devide responses
            resp_count = Response.objects.filter(process__id=self.object_id).count()
            return int(resp_count / forms_count)


    def get_responses(self):
        if self.content_type.model_class() is Form:
            return Response.objects.filter(form__id=self.object_id)
        
        if self.content_type.model_class() is Process:
            resps = Response.objects.filter(process__id=self.object_id)
            return resps

    def get_absolute_url(self):
        pass
    
    def __str__(self):
        return f"Report object {self.content_object} "
    
