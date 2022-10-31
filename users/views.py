from rest_framework import exceptions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from common.utils import slug_to_name
from users import serializers, models
from users.permissions import IsLogOut
from pantries.models import Pantry


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
            Pantry.objects.create(user=user)
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
        slug_nickname = slug_to_name(nickname)
        try:
            user = models.User.objects.get(nickname=slug_nickname)
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        except models.User.DoesNotExist:
            raise exceptions.NotFound


class FollowingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, nickname):
        try:
            slug_nickname = slug_to_name(nickname)
            try:
                followee = models.User.objects.get(nickname=slug_nickname)

                followee_list = request.user.followee.all()
                print(followee_list)
                if followee in followee_list:
                    serializer = serializers.FollowingSerializer(
                        followee_list, many=True
                    )
                    print("OK")
                    return Response(serializer.data)
                else:
                    print("OK1")
                    return Response()
            except models.User.DoesNotExist:
                raise exceptions.NotFound
        except models.User.DoesNotExist:
            raise exceptions.NotFound

    def patch(self, request, nickname):
        try:
            slug_nickname = slug_to_name(nickname)
            try:
                followee = models.User.objects.get(nickname=slug_nickname)
                try:
                    if slug_nickname != request.user:
                        followee_list = request.user.followee.all()
                        if followee in followee_list:
                            request.user.followee.remove(followee)
                            return Response({"Following": "Delete"})
                        else:
                            request.user.followee.add(followee)
                            followee.save()
                            return Response({"Following": "Success"})
                    else:
                        raise exceptions.NotFound
                except models.User.DoesNotExist:
                    raise exceptions.NotFound
            except models.User.DoesNotExist:
                raise exceptions.NotFound
        except models.User.DoesNotExist:
            raise exceptions.NotFound
