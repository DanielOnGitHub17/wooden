from django.urls import path
from game import views

urlpatterns = [
    path('<int:site>/', views.play, name="Game"),
    path('end/', views.end_game, name="Game Over"),
    path('score/', views.score, name="Set Score"),
    path('pos/', views.pos, name="Set Position"),
    path('position/', views.position, name="Get Position"),
    path('crack/', views.crack, name="Crack Block"),
]
