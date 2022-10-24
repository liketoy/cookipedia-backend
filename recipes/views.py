from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from recipes import models, serializers
from recipes.permissions import IsWriter


class RecipeViewSet(ModelViewSet):
    queryset = models.Recipe.objects.all().order_by("-created_at")
    serializer_class = serializers.RecipeSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsWriter]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        return serializer.save(writer=self.request.user)

    def list(self, request, *args, **kwargs):
        q = request.GET.get("q", None)
        if q is not None:
            recipes = (
                self.get_queryset()
                .filter(
                    Q(title__icontains=q)
                    | Q(food__icontains=q)
                    | Q(ingredients__icontains=q)
                )
                .distinct()
            )
        else:
            recipes = self.get_queryset()
        paginator = self.paginator
        results = paginator.paginate_queryset(recipes, request)
        serializer = self.get_serializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)
