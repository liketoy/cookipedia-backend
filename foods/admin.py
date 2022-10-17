from .models import Food
from django.contrib import admin

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):

    """Food 어드민에 관한 정의"""

    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name",)

