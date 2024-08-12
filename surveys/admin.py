from django.contrib import admin

from .models import (
    Answer,
    Form,
    FormResponse,
    Process,
    ProcessForm,
    ProcessResponse,
    Question,
)


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


@admin.register(ProcessResponse)
class ProcessResponseAdmin(admin.ModelAdmin):
    pass


@admin.register(FormResponse)
class FormResponseAdmin(admin.ModelAdmin):
    pass
