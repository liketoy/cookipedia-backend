from django.urls import path
from .views import FoodView
from rest_framework.routers import DefaultRouter


app_name = "foods"


router = DefaultRouter()
router.register("api", FoodView)
urlpatterns = router.urls  # viewset을 쓸 경우 사용


# urlpatterns = [ apiView로 할 경우
#     path('api/', FoodView.as_view()),
# ]
