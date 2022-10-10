from django.db import models
from django.contrib.auth.models import User, AbstractUser
from core.models import TimeStampedModel
from django.core.validators import RegexValidator

# Create your models here.


GENDER = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Not to disclose", "Not to disclose"),
)

phoneNumberReg = RegexValidator(
    regex=r"^01([0|1|6|7|8|9]{1,1})-?([0-9]{3,4})-?([0-9]{4})$"
)


class User(AbstractUser):
    nickname = models.CharField(
        max_length=20, unique=True, verbose_name="닉네임", blank=True
    )
    phone_number = models.CharField(
        validators=[phoneNumberReg], max_length=13, unique=True
    )
    avatar = models.ImageField(
        verbose_name="프로필 이미지",
        blank=True,
        upload_to="profile/%Y/%m/%d",
        default="no_image.png",
    )
    gender = models.CharField(choices=GENDER, blank=False, max_length=30)

    def __str__(self):
        return f"{self.username}"


User._meta.get_field("email")._unique = True
User._meta.get_field("email").blank = False
User._meta.get_field("email").null = False
