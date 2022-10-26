from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from common.utils import slug_to_name
from common.paginators import CustomResultsSetPagination
from pantries import models, serializers
from users.models import User
from pantries.permissions import IsOwner


class PantryView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        pantry = models.Pantry.objects.all()
        paginator = CustomResultsSetPagination()
        results = paginator.paginate_queryset(pantry, request)
        serializer = serializers.PantrySerializer(
            results, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)


class MyPantryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        pantry = user.pantry
        serializer = serializers.PantrySerializer(pantry, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.StoreIngredientSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            pantry = user.pantry
            try:
                serializer.save(pantry=pantry)
                serializer = serializers.PantrySerializer(
                    pantry, context={"request": request}
                )
                return Response(serializer.data)
            except Exception as e:
                raise exceptions.ParseError(e)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        pantry = user.pantry
        pantry.ingredients.clear()
        serializer = serializers.PantrySerializer(pantry, context={"request": request})
        return Response(serializer.data)

    def patch(self, request):
        store_ingredients = request.data.get("ingredients")
        user = request.user
        pantry = user.pantry
        ingredients = models.StoreIngredient.objects.filter(
            pk__in=store_ingredients, pantry=pantry
        )
        if ingredients.exists():
            ingredients.delete()
        serializer = serializers.PantrySerializer(pantry, context={"request": request})
        return Response(serializer.data)


class StoreIngredientInPantryView(APIView):

    permission_classes = [IsOwner]

    def put(self, request, pk):
        try:
            ingredient = models.StoreIngredient.objects.get(pk=pk)
            serializer = serializers.StoreIngredientSerializer(
                ingredient, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                pantry_serializer = serializers.PantrySerializer(request.user.pantry)
                return Response(pantry_serializer.data)
            else:
                return Response(serializer.errors)
        except models.StoreIngredient.DoesNotExist:
            raise exceptions.NotFound

    def delete(self, request, pk):
        try:
            ingredient = models.StoreIngredient.objects.get(pk=pk)
            ingredient.delete()
            return Response({"ok": True})
        except models.StoreIngredient.DoesNotExist:
            raise exceptions.NotFound


class PublicPantryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, nickname):
        name = slug_to_name(nickname)
        try:
            user = User.objects.get(nickname=name)
            pantry = user.pantry
            serializer = serializers.PantrySerializer(
                pantry, context={"request": request}
            )
            return Response(serializer.data)
        except User.DoesNotExist:
            raise exceptions.NotFound
