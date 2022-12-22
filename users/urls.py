from django.urls import path
from users import views
from django.conf.urls.static import static
from django.conf import settings


app_name = "users"

urlpatterns = [
    path("", views.SignUpView.as_view()),
    path("me", views.MeView.as_view()),
    path("login", views.LogInView.as_view()),
    path("logout", views.LogOutView.as_view()),
    path("password", views.ChangePasswordView.as_view()),
    path("@<str:nickname>", views.PublicUserView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
