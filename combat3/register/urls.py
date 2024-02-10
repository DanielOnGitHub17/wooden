from django.contrib import admin
from django.urls import path

from register import views

urlpatterns = [
    path("sign/<str:which>/", views.register_page, name="Signings"),
    path("log/", views.log, name="Account"),
]