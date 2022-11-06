from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.db.models import Q
from notifications.views import create_notification
from recipes import models, serializers
from recipes.permissions import IsWriter
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from pantries.models import Pantry
from ingredients.models import Ingredient


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

    @action(detail=True, methods=["post"])
    def cooking(self, request, pk):
        user = request.user
        recipe = self.get_object()
        create_notification(
            user,
            user,
            "cooking",
            food=recipe.food,
            recipe=recipe,
            preview=f"{recipe} 요리 시작",
        )
        return Response({"ok": True})


class RecipeRecommendView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        pantry = Pantry.objects.get(user=user)
        myingredients = pantry.ingredients.all()

        recipes = models.Recipe.objects.all()
        recommend_list = []
        for recipe in recipes:
            recipe_ingredients = models.TypeIngredient.objects.filter(
                recipe=recipe, type="main"
            )
            result = []
            for recipe_ingredient in recipe_ingredients:
                ingredient = Ingredient.objects.filter(name=recipe_ingredient)
                result += ingredient

            for myingredient in myingredients:
                if myingredient in result:
                    recommend_list.append(recipe)

        recommend_list = set(recommend_list)
        serializer = serializers.RecommendSerializer(recommend_list, many=True)
        return Response({"Recommend_Recipes": serializer.data})

    # 팬트리 안 재료와 레시피의 주재료의 일치 개수에 따라 나열하면 좋을 듯(개선사항)
    # 주재료 일치가 아무것도 없을때는 어쩌징..(개선사항)
