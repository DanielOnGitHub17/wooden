from django.urls import path
from game import views

urlpatterns = [
    path("play/", views.play, name="play"),
    path("practice/", views.practice, name="practice"),
    path("join/", views.JoinGame.as_view(), name="join"),
    path("end/", views.EndGame.as_view(), name="end"),
    path("leave/", views.LeaveGame.as_view(), name="leave"),
    path("start/", views.StartEarly.as_view(), name="start"),
]
