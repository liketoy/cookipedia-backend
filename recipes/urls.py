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
    path(
        "<int:pk>/cooking",
        views.RecipeViewSet.as_view(
            {
                "post": "cooking",
            }
        ),
    ),
    path("<int:id>/likes", views.RecipeLikeView.as_view()),
    path("recommendations", views.RecipeRecommendationView.as_view()),
]
