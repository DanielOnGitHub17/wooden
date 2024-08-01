from django.urls import path

from chat import views

urlpatterns = [
    path("chat/", views.chat, name="Chats")
]