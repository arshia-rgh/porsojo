from django.contrib import admin

from .models import Answer, Form, Process, ProcessForm, Question


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    pass


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    pass


@admin.register(ProcessForm)
class ProcessFormAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass
