from rest_framework import permissions, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from notifications.views import create_notification
from recipes import models, serializers
from recipes.permissions import IsWriter
from common.utils import custom_send_mail


class MailtestView(APIView):
    def get(self, request):
        custom_send_mail()
        return Response({"ok": True})

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


class RecipeLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, id):
        user = request.user
        recipe = get_object_or_404(models.Recipe, pk=id)
        if recipe.writer == user:
            raise exceptions.ParseError("자신의 게시글에 좋아요를 누를 수 없어요!")
        try:
            user = recipe.likes_user.get(pk=user.pk)
            recipe.likes_user.remove(user)
            recipe.save()

            # 동일한 notification 인스턴스 생성 방지를 위함
            delete_notification = recipe.notifications.get(creator=user)
            delete_notification.delete()

        except Exception:
            recipe.likes_user.add(user)
            create_notification(
                user,
                recipe.writer,
                "like",
                food=recipe.food,
                recipe=recipe,
                preview=f"{user}님이 회원님의 레시피를 좋아합니다.",
            )
        return Response({"likes_user": recipe.likes_user.count(), "ok": True})


class RecipeRecommendationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):  # url: recommendations?q=un~~&n=2
        q = request.GET.get("q", "hans_recommendation")
        if q == "hans_recommendation":
            n = request.GET.get("n", None)
            user = request.user
            user_ingredients = user.pantry.ingredients.all()

            qs = (
                models.Recipe.objects.filter(ingredients__in=user_ingredients)
                .distinct()
                .values("pk")
                .annotate(count=Count("pk"))
            )

            pk_array = []
            if n is None:
                # 내가 가진 재료로 충분히 만들 수 있는 레시피들
                for object in qs:
                    if (
                        models.Recipe.objects.get(pk=object["pk"]).ingredients.count()
                        == object["count"]
                    ):
                        pk_array.append(object["pk"])
            else:
                # n에 입력된 수만큼 재료가 있으면 만들 수 있는 레시피들
                n = int(n)
                for object in qs:
                    if (
                        models.Recipe.objects.get(pk=object["pk"]).ingredients.count()
                        == object["count"] + n
                    ):
                        pk_array.append(object["pk"])
            recipes = models.Recipe.objects.filter(pk__in=pk_array)

            if not recipes:
                return Response({"ok": False})

            if n is None:
                serializer = serializers.RecipeSerializer(recipes, many=True)
            else:
                serializer = serializers.IngredientsNeededSerializer(
                    recipes, many=True, context={"user_ingredients": user_ingredients}
                )

            return Response(serializer.data)
