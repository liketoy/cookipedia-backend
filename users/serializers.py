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
    avatar = serializers.ImageField(max_length=None, use_url=True, required=False)

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
# 메서드 validate_필드이름 하면 해당 필드 검증
# 메서드 validate 는 필드 2개이상
