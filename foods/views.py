from django.shortcuts import render
from .serializers import FoodSerializer
from .models import Food
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets  # status로 상태값 커스텀가능

# Create your views here.


# class FoodView(APIView):
#     def get(self, request):  # APIView의 메서드 오버라이드
#         foods = Food.objects.all()
#         foodjson = FoodSerializer(foods, many=True).data
#         print(foodjson)
#         return Response(foodjson, status.HTTP_200_OK)
#         return


class FoodView(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
