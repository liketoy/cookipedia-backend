from django.contrib import admin
from recipes.models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Recipe 어드민에 관한 정의"""

    list_display = ("title", "food", "writer")
    search_fields = ("title", "food__name", "ingredient__name")
    filter_horizontal = ("ingredients",)
