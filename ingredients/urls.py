from django.urls import path
from ingredients import views


app_name = "ingredients"

urlpatterns = [
    path(
        "",
        views.IngredientViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "<int:pk>",
        views.IngredientViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    path("search", views.IngredientViewSet.as_view({"get": "search"})),
    path("categories", views.IngredientViewSet.as_view({"get": "categories"})),
]
                                            