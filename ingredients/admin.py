from django.contrib import admin
from .models import Ingredient

# Register your models here.


@admin.register(Ingredient)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    search_fields = ("name",)
    list_filter = ("category", )