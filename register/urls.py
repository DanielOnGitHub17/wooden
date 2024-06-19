from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path

from register import views

# to make things easier, I might include django.contrib.auth.urls
urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="Sign up"),
    path("signin/", views.SignIn.as_view(), name="Log in"),
    path("signout/", views.SignOut.as_view(), name="Log out"),
]