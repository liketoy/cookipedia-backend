from django.contrib import admin
from .models import Pantry

# Register your models here.


class IngredientList(admin.TabularInline):
    model = Pantry.ingredients.through
    fields = ("ingredient", "date_bought", "status_ingredient")
    readonly_fields = ("status_ingredient",)
    extra = 1


@admin.register(Pantry)
class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        ((None, {"fields": ("user",)})),
    )
    list_display = (
        "__str__",
        "count_ingredients",
    )
    inlines = (IngredientList,)
    search_fields = ('user__nickname',) # 포린키 접근시  '포린키__필드명'