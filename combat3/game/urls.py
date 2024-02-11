from django.urls import path
from game import views


path('', views.game, "Game")