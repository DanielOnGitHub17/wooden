from django.urls import path

from register import views

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="Sign up"),
    path("activate/<str:uidb64>/<str:token>/", views.activate, name="Activate"),
    path("signin/", views.SignIn.as_view(), name="Log in"),
    path("signout/", views.SignOut.as_view(), name="Log out"),
    path("password_reset/", views.ResetPassword.as_view(), name="Reset password"),
    path("password_reset_done/", views.DoneResetPassword.as_view(), name="password_reset_done"),
    path("password_reset_confirm/<str:uidb64>/<str:token>/", views.ConfirmResetPassword.as_view(), name="password_reset_confirm"),
]