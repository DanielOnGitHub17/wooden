"""
URL configuration for wooden project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(os.getenv("DJANGO_ADMIN_URL"), admin.site.urls),
    path("", include("homepage.urls"), name="General"),
    path("", include("register.urls"), name="Registration"),
    path("", include("chat.urls"), name="Chats"),
    path("", include("lounge.urls"), name="Lounge"),
    path("", include("game.urls"), name="Game"),
]
