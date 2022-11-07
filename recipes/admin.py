from django.contrib import admin
from recipes.models import Recipe, TypeIngredient, RecipeEvaluation

class RecipeIngredientAdmin(admin.TabularInline):
    model = TypeIngredient

class RecipeEvaluationAdmin(admin.TabularInline):
    model = RecipeEvaluation
    classes = ['collapse']

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Recipe 어드민에 관한 정의"""

    inlines = [
        RecipeIngredientAdmin,
        RecipeEvaluationAdmin
    ]
    list_display = ("title", "food", "writer")
    search_fields = ("title", "food__name", "ingredients__name")
    filter_horizontal = ("likes_user", )