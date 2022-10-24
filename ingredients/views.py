from rest_framework import exceptions, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from ingredients import serializers, models


class IngredientViewSet(ModelViewSet):
    serializer_class = serializers.IngredientSerializer
    queryset = models.Ingredient.objects.all()

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        category = request.GET.get("category", None)
        if category is None:
            raise exceptions.ParseError("category 값이 비어있습니다.")
        category = category.replace("-", ", ")
        ingredients = self.queryset.filter(category=category).order_by("name")
        paginator = self.paginator
        results = paginator.paginate_queryset(ingredients, request)
        serializer = self.get_serializer(results, many=True)

        return paginator.get_paginated_response(serializer.data)

    @action(detail=False, methods=["get"])
    def search(self, request):
        q = request.GET.get("q", None)
        if q is None:
            raise exceptions.ParseError
        ingredients = self.queryset.filter(name__icontains=q)
        if ingredients.count() == 0:
            raise exceptions.NotFound
        serializer = self.get_serializer(ingredients, many=True)
        return Response(serializer.data)
