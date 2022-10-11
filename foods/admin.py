from django.contrib import admin
from foods.models import Food


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):

    """Food 어드민에 관한 정의"""

    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name",)
