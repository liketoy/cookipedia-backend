from django.contrib import admin
from ingredients.models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    """Ingredient 어드민에 관한 정의"""

    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name",)
