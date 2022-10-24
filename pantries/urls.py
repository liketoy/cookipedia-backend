from django.urls import path
from pantries import views

app_name = "pantries"

urlpatterns = [
    path("", views.PantryView.as_view()),
    path("me", views.MyPantryView.as_view()),
    path("me/<int:pk>", views.StoreIngredientInPantryView.as_view()),
    path("@<str:nickname>", views.PublicPantryView.as_view()),
]
