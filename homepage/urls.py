from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="Home"),
    path("game_help/", views.game_help, name="Game Help"),
    path("dev/", views.dev, name="Developers"),
    path("support/", views.Support.as_view(), name="Support"),
]