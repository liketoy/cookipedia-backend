from django.db import models
from common.models import TimeStampedModel


class Notification(TimeStampedModel):
    """Notification 모델 정의"""

    class NotificationKindChoices(models.TextChoices):
        LIKE = ("like", "좋아요")
        FOLLOW = ("follow", "팔로우")
        COOKING = ("cooking", "요리")
        CERTIFICATION = ("certification", "인증")

    kind = models.CharField(max_length=20, choices=NotificationKindChoices.choices)
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
    is_certificated = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.to} - {self.kind} 알림"

    # 궁금한 점: "is_completed"는 cooking이 완료되었다는 건가? 인증까지 완료된건가?
    # 궁금한 점: certification 알람은 인증을 하라는 알람일까 인증이 완료되었다는 알람일까?
