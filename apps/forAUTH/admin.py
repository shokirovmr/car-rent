from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.forAUTH import exclude_user
from apps.forAUTH.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "fullname", "phone"]
    search_fields = ["username", "fullname", "phone"]
    fieldsets = (
        (None, {"fields": ("fullname", "phone", "username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "avatar",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("fullname", "username", "phone", "password1", "password2"),
            },
        ),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return exclude_user(qs)
