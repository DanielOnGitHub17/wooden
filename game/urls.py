from django.urls import path
from game import views

urlpatterns = [
    path("", views.GamePlay.as_view(), name="Game Play"),
    path("join/", views.JoinGame.as_view(), name="Join Game"),
    path("end/", views.EndGame.as_view(), name="End Game")
]
