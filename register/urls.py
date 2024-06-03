from django.contrib import admin
from django.urls import path

from register import views

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="Sign up"),
    path("signin/", views.SignIn.as_view(), name="SIgn in"),
    path("signout/", views.SignOut.as_view(), name="SIgn in"),
    path("sprite.png", views.profile_pic, name="Profile picture"),
]