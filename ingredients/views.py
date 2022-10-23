from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import Ingredient

# from django.db.models import Q


# Create your views here.
class MakeIngredientView(APIView):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            serializer = serializers.IngredientSerializer(data=request.data)
            if serializer.is_valid():
                ingredient = serializer.save()
                ingredient.save()
                ingredient_serializer = serializers.IngredientSerializer(ingredient)
                return Response(ingredient_serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response(serializer.errors)

    def get(self, request):
        ingredient_list = Ingredient.objects.all()
        serializer = serializers.IngredientSerializer(ingredient_list, many=True).data
        return Response(serializer)


class IngredientDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        ingredient_detail = Ingredient.objects.get(id=pk)
        serializer = serializers.IngredientSerializer(ingredient_detail)
        return Response(serializer.data)

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

    def delete(self, request, pk):
        ingredient_detail = Ingredient.objects.get(id=pk)
        ingredient_detail.delete()
        return Response({"ok": True})


class SearchIngredientView(APIView):
    def get(self, request):
        if "q" not in request.GET:
            return Response({"검색어를 입력하세요"})
        q = request.GET["q"]
        # search_ingredient = Ingredient.objects.get(name=q)
        queryset = Ingredient.objects.all()
        for ingredient in queryset:
            if ingredient.name == q:
                serializer = serializers.IngredientSerializer(ingredient)
                return Response(serializer.data)
        return Response({"그런 재료 없습니다."})
