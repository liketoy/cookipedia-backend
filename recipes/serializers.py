from rest_framework import serializers
from . import models
from ingredients.serializers import IngredientSerializer
from foods.serializers import FoodSerializer


class RecipeSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(use_url=True, required=False) # POST 요청시 빈 값을 허용
    
    class Meta:
        model = models.Recipe
        fields = "__all__"
        read_only_fields = ("created_at", "modified_at", )
    
    def to_representation(self, instance):
        #이 함수가 없을 경우 post 요청 시 food와 ingredients를 딕셔너리 형태로 모든 필드 값을 줘야 한다. 
        
        self.fields['food'] = FoodSerializer(read_only=True)
        self.fields['ingredients'] = IngredientSerializer(many=True, read_only=True)
        return super(RecipeSerializer, self).to_representation(instance)