from django.db import models
from common.models import TimeStampedModel


class Notification(TimeStampedModel):
    """Notification 모델 정의"""

    class NotificationKindChoices(models.TextChoices):
        LIKE = ("like", "좋아요")
        FOLLOW = ("follow", "팔로우")
        COOKING = ("cooking", "요리")
        CERTIFICATION = ("certification", "인증")

    kind = models.CharField(max_length=10, choices=NotificationKindChoices.choices)
    creator = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="creator"
    )
    to = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="to")
    food = models.ForeignKey(
        "foods.Food",
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
    )
    recipe = models.ForeignKey(
        "recipes.Recipe",
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True,
    )
    preview = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.to} - {self.kind} 알림"
