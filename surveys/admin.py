from django.contrib import admin

from .models import Form, Process, ProcessForm, Response


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    pass


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    pass


@admin.register(ProcessForm)
class ProcessFormAdmin(admin.ModelAdmin):
    pass


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    pass


# Register your models here.
