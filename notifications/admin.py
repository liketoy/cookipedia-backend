from django.contrib import admin
from notifications import models


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Notification 어드민 정의"""

    list_display = ("creator", "to", "kind")
