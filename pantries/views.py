# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from .models import Pantry, StoreIngredient


class PantryListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        pantry_list = Pantry.objects.all()
        serializer = serializers.PantryListSerializer(pantry_list, many=True)
        return Response(serializer.data)

    # 팬트리 리스트 조회


class MyPantryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        pantry, _ = Pantry.objects.get_or_create(user=user)
        serializer = serializers.PantrySerializer(pantry)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.StoreIngredientSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            pantry = user.pantry
            serializer.save(pantry=pantry)
            serializer = serializers.PantrySerializer(pantry)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        pantry_ingredients = request.user.pantry.ingredients
        pantry_ingredients.clear()
        return Response({"delete all products"})

    # 로그인한 유저의 팬트리에 담긴 재료들 전체 비우기


class PantryIngredientUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    # def get(self, request, pk):
    #     user = request.user
    #     pantry = Pantry.objects.get(user=user)
    #     queryset = StoreIngredient.objects.filter(pantry=pantry)
    #     for ingredient in queryset:
    #         if ingredient.pk == pk:
    #             serializer = serializers.ReadOnlyStoreIngredientSerializer(ingredient)
    #             return Response(serializer.data)
    #     return Response({"니 장바구니에 없는 재료임."})

    # 로그인한 유저의 팬트리에 담긴 재료의 값 수정전 조회

    def put(self, request, pk):
        user = request.user
        pantry = Pantry.objects.get(user=user)
        queryset = StoreIngredient.objects.filter(pantry=pantry)
        for ingredient in queryset:
            if ingredient.pk == pk:
                serializer = serializers.ReadOnlyStoreIngredientSerializer(
                    ingredient, data=request.data, partial=True
                )
        if serializer.is_valid():
            edited_pantry_ingredient = serializer.save()
            serializer = serializers.ReadOnlyStoreIngredientSerializer(
                edited_pantry_ingredient
            )
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    # 로그인한 유저의 팬트리에 담긴 재료의 값 수정

    def delete(self, request, pk):
        user = request.user
        pantry = Pantry.objects.get(user=user)
        queryset = StoreIngredient.objects.filter(pantry=pantry)
        for ingredient in queryset:
            if ingredient.pk == pk:
                ingredient.delete()
                return Response({"delete success"})

    # 로그인한 유저의 재료 삭제
