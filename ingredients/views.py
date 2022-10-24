from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from . import serializers
from .models import Ingredient


# Create your views here.
class IngredientView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        if "category" not in request.GET:
            return Response({"분류항목을 입력하세요"})
        category = request.GET["category"].replace("-", ", ")
        print(category)
        queryset = Ingredient.objects.filter(category=category)
        if not queryset:
            return Response({"해당 분류항복인 재료는 없습니다."})
        serializer = serializers.IngredientSerializer(queryset, many=True)
        return Response(serializer.data)

    # 재료 리스트 조회 (category값에 따라 다름)

    def post(self, request):
        serializer = serializers.IngredientSerializer(data=request.data)
        if serializer.is_valid():
            ingredient = serializer.save()
            serializer = serializers.IngredientSerializer(ingredient)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    # 재료 생성


class IngredientDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        ingredient_detail = Ingredient.objects.get(id=pk)
        serializer = serializers.IngredientSerializer(ingredient_detail)
        return Response(serializer.data)

    # 재료 정보 조회

    def put(self, request, pk):
        ingredient_detail = Ingredient.objects.get(id=pk)
        serializer = serializers.IngredientSerializer(
            ingredient_detail, data=request.data, partial=True
        )
        if serializer.is_valid():
            edited_ingredient = serializer.save()
            serializer = serializers.IngredientSerializer(edited_ingredient)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    # 재료 정보 수정

    def delete(self, request, pk):
        ingredient_detail = Ingredient.objects.get(id=pk)
        ingredient_detail.delete()
        return Response({"ok": True})

    # 재료 삭제


class SearchIngredientView(APIView):
    def get(self, request):
        q = request.GET.get("q", None)
        if q is None:
            return Response({"검색어를 입력하세요"})
        queryset = Ingredient.objects.filter(name__contains=q)
        if not queryset:
            return Response({"그런 재료 없습니다."})
        serializer = serializers.IngredientSerializer(queryset, many=True)
        return Response(serializer.data)

    # 재료 검색 (q-name에 따라 다름)
