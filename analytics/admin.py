from django.contrib import admin

from analytics.models.activities import UserActivity


class UserActivityAdmin(admin.ModelAdmin):
    model = UserActivity

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def has_add_permission(self, request, obj=None) -> bool:
        return True

    def has_change_permission(self, request, obj=None) -> bool:
        return False


admin.site.register(UserActivity, UserActivityAdmin)