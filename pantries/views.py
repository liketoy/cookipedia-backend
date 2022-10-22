from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import models, serializers
from rest_framework import status


class MyPantryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        pantry, _ = models.Pantry.objects.get_or_create(
            user=user
        )  # 두번째 변수는 get인지 create인지에 대한 불리언값
        serializer = serializers.PantrySerializer(pantry)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        serializer = serializers.StoreIngredientSerializer(data=request.data)
        if serializer.is_valid():
            pantry = user.pantry  # 원투원관계라서 가능
            serializer.save(pantry=pantry)
            serializer = serializers.PantrySerializer(
                pantry
            )  # serializers.PantrySerializer에서 obj가 여기서 만든 pantry로
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
