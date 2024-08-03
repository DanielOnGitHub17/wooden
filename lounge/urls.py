from django.urls import path

from lounge import views


urlpatterns = [
    path("", views.Lounge.as_view(), name="Lounge"),
]