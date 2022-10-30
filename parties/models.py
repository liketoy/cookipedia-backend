from django.db import models
from common.models import TimeStampedModel

# Create your models here.


class Party(TimeStampedModel):
    users = models.ManyToManyField("users.User", related_name="parties")
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "parties"
        
    def __str__(self):
        return f"{self.name}"


class Invitation(TimeStampedModel):
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    invitee = models.ForeignKey("users.User", on_delete=models.CASCADE)
