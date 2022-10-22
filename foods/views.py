from . import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from django.db.models import Q

from foods import serializers  # status로 상태값 커스텀가능

# Create your views here.


# class FoodView(APIView):
#     def get(self, request):  # APIView의 메서드 오버라이드
#         foods = Food.objects.all()
#         foodjson = FoodSerializer(foods, many=True).data
#         print(foodjson)
#         return Response(foodjson, status.HTTP_200_OK)


class FoodListView(APIView):
    def get(self, request):
        if not "category" in request.GET:
            raise exceptions.ParseError("category 값을 입력해 주세요.")
        foods = models.Food.objects.filter(category=request.GET.get("category"))
        serializer = serializers.FoodSerializer(foods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            raise exceptions.ParseError("회원만 등록이 가능합니다.")
        serializer = serializers.FoodSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class FoodDetailView(APIView):
    def get(self, request, pk):
        try:
            food = models.Food.objects.get(id=pk)
        except models.Food.DoesNotExist:
            raise exceptions.ParseError("등록되지 않은 음식입니다.")
        serializer = serializers.FoodSerializer(food)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            food = models.Food.objects.get(id=pk)
        except models.Food.DoesNotExist:
            raise exceptions.ParseError("수정 실패, 등록되지 않은 음식입니다.")
        serializer = serializers.FoodSerializer(food, data=request.data, partial=True)
        if serializer.is_valid():  # 잘못된 키를 줘도 True가 된다 ex) {"nam": "음식이름"}
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise exceptions.ParseError("수정 실패, 입력값이 올바르지 않습니다.")

    def delete(self, request, pk):
        try:
            food = models.Food.objects.get(id=pk)
            food.delete()
        except models.Food.DoesNotExist:
            raise exceptions.ParseError("삭제 실패, 존재하지 않는 음식입니다.")


class FoodSearchView(APIView):
    def get(self, request):
        if not "q" in request.GET:
            return Response(
                {"ok": "검색 실패, q값을 입력해 주세요."}, status=status.HTTP_400_BAD_REQUEST
            )
        q = Q().add(Q(name__icontains=request.GET.get("q")), Q.AND)
        foods = models.Food.objects.filter(q)
        if not foods:
            return Response(
                {"ok": "검색 실패, 게시물이 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = serializers.FoodSerializer(foods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
