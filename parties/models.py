from django.db import models
from common.models import TimeStampedModel


# Create your models here.
class Party(TimeStampedModel):
    name = models.CharField(max_length=40, unique=True)
    host = models.ForeignKey(
        "users.User", related_name="host", on_delete=models.CASCADE
    )
    members = models.ManyToManyField("users.User", related_name="member")
    adress = models.TextField()
    # description = models.TextField()


class Invitation(TimeStampedModel):
    party = models.ForeignKey(Party, on_delete=models.CASCADE)
    invite = models.ManyToManyField("users.User", related_name="invite")
    agree = models.BooleanField(default=False)
