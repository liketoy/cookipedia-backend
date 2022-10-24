from django.urls import path
from recipes import views

app_name = "recipes"

urlpatterns = [
    path(
        "",
        views.RecipeViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "<int:pk>",
        views.RecipeViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
]