from django.contrib import admin
from certification import models

# Register your models here.


@admin.register(models.Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("food", "status")
