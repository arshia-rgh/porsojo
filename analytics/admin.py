from django.contrib import admin
from analytics.models.activities import UserActivity
from analytics.models.report import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass


class UserActivityAdmin(admin.ModelAdmin):
    model = UserActivity

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        return True

    def has_change_permission(self, request, obj=None) -> bool:
        return False


admin.site.register(UserActivity, UserActivityAdmin)