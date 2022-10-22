from django.urls import path
from rest_framework.routers import DefaultRouter
from users import views

app_name = "users"

urlpatterns = [
    path("me", views.MeView.as_view()),
    path("", views.SignUpView.as_view()),
    path("login", views.LoginView.as_view()),
    path("logout", views.LogoutView.as_view()),
    path("password", views.ChangePasswordView.as_view()),
]
