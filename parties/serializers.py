from rest_framework import serializers
from . import models
from users.serializers import TinyRelatedUserSerializer


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Party
        fields = ("users", "host", "name", "description")

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.update(
            {
                "users": TinyRelatedUserSerializer(
                    instance.users, many=True, read_only=True
                ).data,
                "host": TinyRelatedUserSerializer(instance.host, read_only=True).data,
            }
        )
        return response


class InvitationSerializer(serializers.ModelSerializer):
    party_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Invitation
        fields = ("party_info",)

    def get_party_info(self, obj):
        serializer = PartySerializer(obj.party)
        return serializer.data

