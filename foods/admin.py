from django.contrib import admin
from .models import Food
# Register your models here.


@admin.register(Food)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    search_fields = ("name",)
    list_filter = ("category", )