from django.urls import path
from game import views

urlpatterns = [
    path('<int:site>/', views.play, name="Game"),
    path('end/', views.end_game, name="Game Over"),
    path('score/', views.score, name="Set Score"),
]
