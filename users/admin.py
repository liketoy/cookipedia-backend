from django.contrib import admin
from .models import User

# Register your models here.


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "avatar",
                    "username",
                    "password",
                    "name",
                    "nickname",
                    "email",
                    "gender",
                    "address",
                    "birth_date",
                    "phone_number",
                )
            },
        ),
        (
            "Permissions",
            {
                "classes": ("collapse",),
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Important Dates",
            {
                "classes": ("collapse",),
                "fields": (
                    "last_login",
                    "date_joined",
                ),
            },
        ),
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    list_display = ("username", "email", "name")
    search_fields = ("username", "email", "name")
