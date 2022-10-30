from django.shortcuts import render, get_object_or_404
from rest_framework import status, exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from users.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from . import models
from common.utils import slug_to_name

# Create your views here.


class PartyListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        parties = models.Party.objects.filter(users=user)

        if not parties:
            return Response("가입된 파티가 없습니다.", status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.PartySerializer(parties, many=True)
        return Response(serializer.data)


class MyInvitationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        invitations = models.Invitation.objects.filter(invitee=user)

        # 같은 파티에 대한 중복 초대장 방지/ 자기 자신 초대 방지
        to_be_deleted = []
        for invitation in invitations:
            if invitation.party.host == user:
                to_be_deleted.append(invitation)
            elif invitations.filter(party__pk=invitation.party.pk).count() >= 2:
                to_be_deleted.append(invitation)
            invitations = invitations.exclude(pk__in=[el.pk for el in to_be_deleted])

        if not invitations:
            return Response("초대장이 없습니다.", status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.InvitationSerializer(invitations, many=True)
        return Response(serializer.data)


class InviteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id, nickname):
        invitee = get_object_or_404(User, nickname=nickname)
        host = request.user
        host_parties = models.Party.objects.filter(host=host)
        if host_parties:
            party = get_object_or_404(host_parties, pk=id)

            if invitee not in party.users.all():
                if not models.Invitation.objects.filter(
                    party=party, invitee=invitee
                ).exists():
                    models.Invitation.objects.create(party=party, invitee=invitee)
                else:
                    raise exceptions.ParseError("초대는 한 번만 가능함..ㅠㅠ")
            else:
                raise exceptions.ParseError("이미 가입된 유저임...")

        else:
            raise exceptions.ParseError("초대 가능한 파티가 없어요!")

        return Response("초대장을 보냈어요!")


class InvitationAcceptanceView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        invitee = request.user
        party = get_object_or_404(models.Party, id=id)
        
        if invitee in party.users.all():  # 미구현
            print(0)
        else:
            print(1)
        return Response()
        
    def put(self, request, id):
        invitee = request.user
        try:
            party = models.Party.objects.get(pk=id)
            invitation = models.Invitation.objects.get(invitee=invitee, party=party)
        except Exception:
            raise exceptions.ParseError("존재하지 않는 파티/초대 입니다.")
        
        if request.data.get("acceptance") == True:
            result = "accepted"
            party.users.add(invitee)
        else:
            result = "rejected"
        invitation.delete()
        
        return Response({"result": result})
