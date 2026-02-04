"""URLs for the lounge app."""

from django.urls import path

from lounge import views

urlpatterns = [
    path("lounge/", views.Lounge.as_view(), name="Lounge"),
]
