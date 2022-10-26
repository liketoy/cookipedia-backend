from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.user)

    # obj에는 pk에 맞는 재료의 storeingredient와 연결되어있는 pantry가 들어와야 함.ㄴ
