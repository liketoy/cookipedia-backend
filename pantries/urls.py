from django.urls import path
from . import views

app_name = "pantries"

urlpatterns = [
    path("me", views.MyPantryView.as_view()),
    
]
