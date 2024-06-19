from django.urls import path

from lounge import views


urlpatterns = [
    path("", views.Lounge.as_view(), name="Lounge"),
    path("create/", views.create_game, name="Create Game"),
    path("join/<int:site>", views.join_game, name="Join Game"),
]