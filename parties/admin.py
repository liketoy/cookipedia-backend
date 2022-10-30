from django.contrib import admin
from .models import Party, Invitation

# Register your models here.


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    filter_horizontal = ("users",)


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    search_fields = ("party__name",)
