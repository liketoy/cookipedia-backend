# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from .models import Pantry, StoreIngredient


class PantryListView(APIView):
    def get(self, request):
        pantry_list = Pantry.objects.all()
        serializer = serializers.PantryListSerializer(pantry_list, many=True)
        return Response(serializer.data)


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


class PantryIngredientUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        pantry = Pantry.objects.get(user=user)
        queryset = StoreIngredient.objects.filter(pantry=pantry)
        for ingredient in queryset:
            if ingredient.pk == pk:
                serializer = serializers.ReadOnlyStoreIngredientSerializer(ingredient)
                return Response(serializer.data)
        return Response({"니 장바구니에 없는 재료임."})

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

    def delete(self, request, pk):
        user = request.user
        pantry = Pantry.objects.get(user=user)
        queryset = StoreIngredient.objects.filter(pantry=pantry)
        for ingredient in queryset:
            if ingredient.pk == pk:
                ingredient.delete()
                return Response({"delete success"})
