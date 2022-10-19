from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter

from .views import users_views

app_name = "api"

urlpatterns = [
    # 회원 url
    path("users/", users_views.UserCreateView.as_view()),
]
