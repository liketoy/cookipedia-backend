from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from common.utils import slug_to_name
from pantries import models, serializers
from users.models import User


class PantryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pantry = models.Pantry.objects.all()
        serializer = serializers.PantrySerializer(pantry, many=True)
        return Response(serializer.data)


class MyPantryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        pantry, _ = models.Pantry.objects.get_or_create(user=user)
        serializer = serializers.PantrySerializer(pantry, context={"request": request})

        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.StoreIngredientSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            pantry = user.pantry
            try:
                serializer.save(pantry=pantry)
                serializer = serializers.PantrySerializer(pantry)
                return Response(serializer.data)
            except Exception as e:
                raise exceptions.ParseError(e)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        pantry = user.pantry
        pantry.ingredients.clear()
        serializer = serializers.PantrySerializer(pantry)
        return Response(serializer.data)


class StoreIngredientInPantryView(APIView):
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
        except User.DoesNotExist:
            raise exceptions.NotFound
        try:
            pantry = user.pantry
        except models.Pantry.DoesNotExist:
            raise exceptions.NotFound
        serializer = serializers.PantrySerializer(pantry)
        return Response(serializer.data)
