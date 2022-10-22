from rest_framework import serializers
from . import models


class PrivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            "username",
            "name",
            "email",
            "nickname",
            "gender",
            "avatar",
            "address",
            "birth_date",
            "phone_number",
        )


class TinyRelatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("avatar", "nickname")
