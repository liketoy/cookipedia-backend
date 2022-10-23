from django.urls import path
from ingredients import views

app_name = "ingredients"

urlpatterns = [
    path("", views.IngredientView.as_view()),
    path("<int:pk>", views.IngredientDetailView.as_view()),
    path("search/", views.SearchIngredientView.as_view()),
]
