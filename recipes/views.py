from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from . import models, serializers
from django.db.models import Q
from foods.serializers import FoodSerializer

# Create your views here.


class RecipeListView(APIView):
    def get(self, request):
        if not "q" in request.GET:  # q가 없는 경우 모든 레시피 리스트
            recipes = models.Recipe.objects.all().order_by("-created_at")
            serializer = serializers.RecipeSerializer(recipes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        keyword = request.GET.get("q")
        q = Q().add(
            Q(title__icontains=keyword)
            | Q(food__name__icontains=keyword)
            | Q(ingredients__name__icontains=keyword),
            Q.OR,
        )
        # 최근 작성된 게시물 순서대로 나열, distinct()로 중복 제거
        recipes = models.Recipe.objects.filter(q).order_by("-created_at").distinct()
        if not recipes:  # q로 필터링된 게시물이 없는 경우
            return Response({"ok": "검색 실패, 게시물이 없습니다."})
        serializer = serializers.RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        if not user:
            return Response(
                {"ok": "회원만 등록할 수 있습니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = serializers.RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeDetailView(APIView):
    def get(self, request, pk):
        try:
            recipe = models.Recipe.objects.get(id=pk)
        except models.Recipe.DoesNotExist:
            raise exceptions.ParseError("등록되지 않는 레시피입니다.")
        serializer = serializers.RecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            recipe = models.Recipe.objects.get(id=pk)
        except models.Recipe.DoesNotExist:
            raise exceptions.ParseError("삭제 실패, 존재하지 않는 레시피입니다.")

        serializer = serializers.RecipeSerializer(recipe, data=request.data, partial=True)
        if serializer.is_valid() and recipe.writer == request.user:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise exceptions.ParseError("수정 실패, 입력값이 올바르지 않거나 해당 레시피의 작성자가 아닙니다.")

    def delete(self, request, pk):
        try:
            recipe = models.Recipe.objects.get(id=pk)
        except models.Recipe.DoesNotExist:
            raise exceptions.ParseError("삭제 실패, 존재하지 않는 레시피입니다.")

        if recipe.writer == request.user:
            recipe.delete()
            return Response({"ok": True})
        else:
            raise exceptions.ParseError("해당 레시피의 작성자만 삭제할 수 있습니다.")
