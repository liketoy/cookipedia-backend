from django.contrib import admin
from pantries.models import StoreIngredient, Pantry


class StoreIngredientInline(admin.TabularInline):
    model = StoreIngredient
    readonly_fields = ("status_ingredient",)


@admin.register(Pantry)
class PantryAdmin(admin.ModelAdmin):
    """Pantry 어드민에 관한 정의"""

    inlines = [
        StoreIngredientInline,
    ]
    list_display = ("__str__", "count_ingredients")
    search_fields = ("user__nickname",)
