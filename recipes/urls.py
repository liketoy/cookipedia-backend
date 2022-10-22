from django.urls import path
from . import views

app_name = "recipes"

urlpatterns = [
    path("", views.RecipeListView.as_view()),
    path("<int:pk>", views.RecipeDetailView.as_view()),
]
