from django.urls import path
from pantries import views

app_name = "pantries"


urlpatterns = [
    path("", views.PantryListView.as_view()),
    path("me", views.MyPantryView.as_view()),
    path("me/<int:pk>", views.PantryIngredientUpdateView.as_view()),
]
