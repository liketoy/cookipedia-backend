from django.urls import path
from . import views

app_name = "parties"


urlpatterns = [
    path("", views.PartyListView.as_view()),
    path("me", views.MyInvitationsView.as_view()),
    path("<int:id>/@<str:nickname>", views.InviteView.as_view()),
    path("<int:id>", views.InvitationAcceptanceView.as_view())
]
