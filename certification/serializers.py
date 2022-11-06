from notifications.models import Notification
from certification.models import Certification
from rest_framework import serializers


class CertificationListSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField()
    food = serializers.StringRelatedField()
    recipe = serializers.StringRelatedField()
    created_at = serializers.StringRelatedField()

    class Meta:
        model = Notification

        fields = (
            "pk",
            "creator",
            "food",
            "recipe",
            "is_completed",
            "created_at",
        )


class CertificationSerializer(serializers.ModelSerializer):
    food = serializers.StringRelatedField()
    recipe = serializers.StringRelatedField()

    class Meta:
        model = Certification

        fields = (
            "food",
            "recipe",
        )
