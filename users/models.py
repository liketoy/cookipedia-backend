from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """사용자 Model에 관한 정의"""

    email = models.EmailField(_("email address"), unique=True)
    nickname = models.CharField(max_length=40, unique=True)
    avatar = models.ImageField(blank=True, null=True, upload_to="avatar/%Y/%m/%d/")
    address = models.CharField(max_length=140)
    birth_date = models.DateField(null=True, blank=True)
    phoneNumberReg = RegexValidator(regex=r"01([0|1|6|7|8|9]{1,1})\d{3,4}\d{4}")
    phone_number = models.CharField(
        validators=[phoneNumberReg], max_length=11, unique=True
    )
