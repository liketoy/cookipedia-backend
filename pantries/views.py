# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from pantries import models, serializers


class MyPantryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        pantry, _ = models.Pantry.objects.get_or_create(user=user)
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
