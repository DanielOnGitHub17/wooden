from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="Home"),
    path("leaders/", views.leaders, name="Leaders"),
    path("game_help/", views.game_help, name="Game Help"),
    path("support/", views.support, name="Support"),
    path("dev/", views.dev, name="Developers"),
]