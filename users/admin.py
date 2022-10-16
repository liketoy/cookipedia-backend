from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.
@admin.register(User)
class UserAdmin(UserAdmin):
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
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ["collapse"],
            },
        ),
        (
            "Important dates",
            {"fields": ("last_login", "date_joined"), "classes": ["collapse"]},
        ),
    )
    list_display = ("username", "email", "name")
    filter_horizontal = [
        "groups",
        "user_permissions",
    ]
