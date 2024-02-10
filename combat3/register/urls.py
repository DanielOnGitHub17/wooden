from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("sign/<str:which>", views.register_page, name="Signings"),
]