from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """사용자 Model에 관한 정의"""

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Not to disclose", "Not to disclose"),
    )

    email = models.EmailField(_("email address"), unique=True)
    first_name = None
    last_name = None
    name = models.CharField(max_length=40)
    nickname = models.CharField(max_length=40, unique=True)
    gender = models.CharField(choices=GENDER_CHOICES, blank=False, max_length=30)
    avatar = models.ImageField(blank=True, null=True, upload_to="avatar/%Y/%m/%d/")
    address = models.CharField(max_length=140)
    birth_date = models.DateField(null=True, blank=True)
    phoneNumberReg = RegexValidator(regex=r"01([0|1|6|7|8|9]{1,1})\d{3,4}\d{4}")
    phone_number = models.CharField(
        validators=[phoneNumberReg], max_length=11, unique=True
    )
