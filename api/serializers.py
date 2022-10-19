from rest_framework import serializers
from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "name",
            "nickname",
            "gender",
            "avatar",
            "address",
            "birth_date",
            "phone_number",
        )
