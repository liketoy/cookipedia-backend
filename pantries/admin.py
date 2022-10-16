from django.contrib import admin
from pantries.models import Pantry, StoreIngredient


# Register your models here.
class PantryInline(admin.TabularInline):
    model = StoreIngredient
    fields = [
        "ingredient",
        "date_bought",
        "status_ingredient",
    ]


@admin.register(Pantry)
class PantryAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "count_ingredients",
    )
    search_fields = ["user"]
    inlines = [
        PantryInline,
    ]
    search_fields = ("user__nickname",)
