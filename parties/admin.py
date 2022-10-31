from django.contrib import admin
from parties.models import Party


# Register your models here.
@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ("name", "host")
    filter_horizontal = ("members",)
    search_fields = ("name",)
