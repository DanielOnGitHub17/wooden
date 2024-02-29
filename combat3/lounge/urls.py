from django.urls import path

from lounge import views


urlpatterns = [
    path("", views.lounge, name="Lounge"),
    path("create/", views.create_game, name="Create Game"),
]