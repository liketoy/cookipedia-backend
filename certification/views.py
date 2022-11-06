from notifications.models import Notification
from certification.models import Certification
from certification import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from datetime import timedelta
from django.utils import timezone


# Create your views here.


class CertificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        print(user)
        certification_list = Notification.objects.filter(creator=user)
        serializer = serializers.CertificationListSerializer(
            certification_list, many=True
        )
        return Response(serializer.data)


class CertificationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = request.user
        try:
            certification = Notification.objects.get(
                pk=pk,
                creator=user,
            )
            if certification.created_at >= timezone.now() - timedelta(hours=24):
                serializer = serializers.CertificationListSerializer(certification)
                return Response(serializer.data)
            else:
                raise exceptions.NotAcceptable("유효시간이 지났습니다.")
        except Notification.DoesNotExist:
            raise exceptions.NotFound("해당 요리를 하지 않았습니다.")

    def post(self, request, pk):
        user = request.user
        try:
            certification = Notification.objects.get(
                pk=pk,
                creator=user,
                is_completed=False,
            )
            if certification.created_at >= timezone.now() - timedelta(hours=24):
                if request.FILES.get("image"):
                    certification_post = Certification.objects.create(
                        food=certification.food,
                        recipe=certification.recipe,
                        photo=request.FILES.get("image"),
                        target=user,
                        status=False,
                    )
                    serializer = serializers.CertificationSerializer(certification_post)
                    serializer.save()
                    certification.is_completed = True
                    certification.save()
                    return Response(serializer.data)
                else:
                    raise exceptions.NotAuthenticated("사진이 없습니다.")
            else:
                raise exceptions.NotAcceptable("유효시간이 지났습니다.")

        except Notification.DoesNotExist:
            raise exceptions.NotFound("인증을 요청했거나, 해당 요리를 하지 않았습니다.")
