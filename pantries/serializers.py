from rest_framework import serializers, exceptions
from django.core.paginator import Paginator
from django.utils import timezone
from pantries import models
from users.serializers import TinyRelatedUserSerializer
from ingredients.serializers import IngredientSerializer


class StoreIngredientSerializer(serializers.ModelSerializer):
    is_status = serializers.SerializerMethodField(read_only=True)
    # date_bought = serializers.DateField(required=False, allow_null=True)
    # expiry_date = serializers.DateField(required=False, allow_null=True)
    
    class Meta:
        model = models.StoreIngredient
        fields = (
            "pk",
            "ingredient",
            "date_bought",
            "expiry_date",
            "is_status",
        )

    def get_is_status(self, obj):
        return self.Meta.model.is_status(obj)

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response.update(
            {"ingredient": IngredientSerializer(instance.ingredient).data}
        )
        return response

    def validate_date_bought(self, data):
        now = timezone.localtime(timezone.now()).date()
        if data is not None and data > now:
            raise serializers.ValidationError("미래에서 사오신 겁니까...?")
        return data
    
    def to_internal_value(self, data):  # 구매일자, 폐기일자의 null값 허용을 위한 함수
        try:
            if data["date_bought"] == "":
                data["date_bought"] = None
            if data["expiry_date"] == "":
                data["expiry_date"] = None
        except:
            pass
        return super(StoreIngredientSerializer, self).to_internal_value(data)


class PantrySerializer(serializers.ModelSerializer):
    user = TinyRelatedUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Pantry
        fields = ("user", "ingredients")

    def get_ingredients(self, obj):
        request = self.context.get("request")
        queryset = models.StoreIngredient.objects.filter(pantry=obj).order_by(
            "created_at"
        )
        page_size = request.query_params.get("page_size", 10)
        page = request.query_params.get("page", 1)
        try:
            paginator = Paginator(queryset, page_size)
            result = paginator.page(page)
            serializer = StoreIngredientSerializer(result, many=True)

            return {"count": queryset.count(), "results": serializer.data}
        except Exception as e:
            raise exceptions.ParseError(e)
