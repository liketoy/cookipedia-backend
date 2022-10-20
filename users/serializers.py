from rest_framework import serializers
from users import models


class TinyRelatedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = (
            "avatar",
            "nickname",
        )


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
