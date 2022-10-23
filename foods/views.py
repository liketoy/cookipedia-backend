from rest_framework import exceptions, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from common.utils import slug_to_name
from foods import serializers, models


class FoodViewSet(ModelViewSet):
    serializer_class = serializers.FoodSerializer
    queryset = models.Food.objects.all()

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        category = request.GET.get("category", None)
        filter_kwargs = {}
        if category is not None:
            category = slug_to_name(category)
            filter_kwargs["category"] = category
        foods = self.queryset.filter(**filter_kwargs)
        serializer = self.get_serializer(foods, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def search(self, request):
        q = request.GET.get("q", None)
        if q is None:
            raise exceptions.ParseError
        foods = self.queryset.filter(name__icontains=q)
        if foods.count() == 0:
            raise exceptions.NotFound
        serializer = self.get_serializer(foods, many=True)
        return Response(serializer.data)
