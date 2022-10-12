from django.contrib import admin
from .models import Recipe

# Register your models here.


@admin.register(Recipe)
class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "cover",
                    "title",
                    "food",
                    "ingredients",
                    "writer",
                    "content",
                )
            },
        ),
    )

    filter_horizontal = ("ingredients",)
    list_display = ("title", "food", "writer")
    search_fields = ("title", "food__name", "ingredients__name")
