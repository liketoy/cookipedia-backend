from django.shortcuts import get_object_or_404
from rest_framework import permissions, exceptions
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from pantries.models import Pantry
from recipes import models, serializers
from recipes.permissions import IsWriter
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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


class RecipeRecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            user_pantry = Pantry.objects.get(user=user)
            user_ingredients = user_pantry.ingredients.all()
        except Exception as e:
            raise exceptions.ParseError(e)

        # 잘못된 값 예시

        # q = Q()
        # for ingredient in user_ingredients:
        #     q.add(Q(pk=ingredient.pk), q.OR)
        # recipes = models.Recipe.objects.filter(q)

        # 위 예시는 recipes = models.Recipe.objects.filter(ingredients__in=user_ingredients)와 결과가 똑같다

        # recipes = models.Recipe.objects.all() 비효율
        recipes = models.Recipe.objects.filter(
            ingredients__in=user_ingredients
        ).distinct()  # 유저가 가진 ingredients 중 하나라도 일치하는 recipes
        for ingredient in user_ingredients:
            recipes = recipes.filter(ingredients__pk=ingredient.pk)

        recommendation_serializer = serializers.RecipeRecommendationSerializer(
            recipes, many=True, context={"user_ingredients": user_ingredients}
        )
        return Response(recommendation_serializer.data)


class RecipeLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, id):
        user = request.user
        recipe = get_object_or_404(models.Recipe, pk=id)

        try:
            user = recipe.likes_user.get(pk=user.pk)
            recipe.likes_user.remove(user)
        except Exception:
            recipe.likes_user.add(user)
        return Response({"likes_user": recipe.likes_user.count(), "ok": True})
