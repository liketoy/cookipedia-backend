from django.shortcuts import render
from users.models import User
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from ..serializers import UserCreateSerializer

# Create your views here.


class UserCreateView(APIView):
    def post(self, request):
        user = User.objects.create_user(
            username=request.data["username"],
            password=request.data["password"],
            email=request.data["email"],
            nickname=request.data["nickname"],
            gender=request.data["gender"],
            avatar=request.data["avatar"],
            address=request.data["address"],
            birth_date=request.data["birth_date"],
            phone_number=request.data["phone_number"],
        )

        user.save()
        token = Token.objects.create(user=user)
        return Response({"Token": token.key}, status=status.HTTP_201_CREATED)

    # def get(self, request):  # 확인용
    #     users = User.objects.all()
    #     usersjson = UserCreateSerializer(users, many=True).data
    #     return Response(usersjson)
