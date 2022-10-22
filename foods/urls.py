from django.urls import path
from . import views
# from rest_framework.routers import DefaultRouter


app_name = "foods"


# router = DefaultRouter()
# router.register("api", FoodView)
# urlpatterns = router.urls  # viewset을 쓸 경우 사용


urlpatterns = [
    path("", views.FoodListView.as_view()),
    path("<int:pk>", views.FoodDetailView.as_view()),
    path("search", views.FoodSearchView.as_view()),
]
