from rest_framework.viewsets import ModelViewSet
from foods import serializers, models


class FoodViewSet(ModelViewSet):
    serializer_class = serializers.FoodSerializer
    queryset = models.Food.objects.all()
