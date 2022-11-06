from django.urls import path
from certification import views

app_name = "certification"

urlpatterns = [
    path("", views.CertificationListView.as_view()),
    path("<int:pk>", views.CertificationView.as_view()),
]
