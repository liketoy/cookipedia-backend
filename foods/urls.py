from django.urls import path
from foods import views

app_name = "foods"

urlpatterns = [
    path(
        "",
        views.FoodViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "<int:pk>",
        views.FoodViewSet.as_view(
            {
                "get": "retrieve",
                "put": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    path("search", views.FoodViewSet.as_view({"get": "search"})),
    path("categories", views.FoodViewSet.as_view({"get": "categories"})),
]
