from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from rest_framework import exceptions, status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout


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
        # user.is_active = False
        # user.save() 하면 delete의 경우 바로 삭제 / is_active를 설정할 경우 유저만 로그인 불가, db엔 유지
        return Response({"ok": True})


class SignUpView(APIView):
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


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise exceptions.ParseError()
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"ok": "로그인 성공"})
        else:
            return Response(
                {"error": "username 혹은 password가 잘못되었습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye"})


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not old_password or not new_password or not confirm_password:
            raise exceptions.ParseError("장난침?")
        if new_password != confirm_password:
            raise exceptions.ParseError("새로운 비밀번호와 비밀번호 확인이 일치하지 않습니다.")
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response({"ok": "변경 완료"})
        else:
            raise exceptions.ParseError("비밀번호가 틀립니다.")
