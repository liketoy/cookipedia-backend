from django.contrib import admin

from recipes.models import Recipe


# Register your models here.
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    filter_horizontal = ("ingredients",)
    list_display = ("title", "food", "writer")
    search_fields = (
        "title",
        "food",
        "ingredients",
    )
