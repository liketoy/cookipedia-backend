from rest_framework import exceptions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from users import serializers, models
from common.utils import slug_to_nickname
from users.permissions import IsLogOut


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user, data=request.data, partial=True
        )
        if serializer.is_valid():
            edited_user = serializer.save()
            serializer = serializers.PrivateUserSerializer(edited_user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"ok": True})


class SignUpView(APIView):

    permission_classes = [IsLogOut]

    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise exceptions.ParseError
        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            user_serializer = serializers.PrivateUserSerializer(user)
            return Response(user_serializer.data)
        else:
            return Response(serializer.errors)


class LogInView(APIView):

    permission_classes = [IsLogOut]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise exceptions.ParseError("장난침?")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"ok": "로그인 성공"})
        else:
            return Response(
                {"error": "username이 잘못됬거나, password가 잘못되었습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogOutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "잘 가시고~"})


class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")
        if not old_password or not new_password or not confirm_password:
            raise exceptions.ParseError("장난 침?")
        if new_password != confirm_password:
            raise exceptions.ParseError("새로운 비밀번호와 비빌번호 확인 일치하지않습니다.")
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response({"ok": "변경완료"})
        else:
            raise exceptions.ParseError("비밀번호가 틀립니다.")


class PublicUserView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, nickname):
        slug_nickname = slug_to_nickname(nickname)
        try:
            user = models.User.objects.get(nickname=slug_nickname)
        except models.User.DoesNotExist:
            raise exceptions.NotFound
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)
