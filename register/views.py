from django.contrib import messages as msg  # Maybe add 'as msg :)'
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView

from game.models import Player
from helpers import handle_error, WoodenError, new_username
from register.forms import SignInForm, SignUpForm

# USE CreateView/ Use Message Mixins instead of request.session/whatever
class SignUp(SuccessMessageMixin, CreateView):
    template_name = "signup.html"
    form_class = SignUpForm
    success_url = "/signin/"
    success_message = "Hello, %(first_name)s. Your account was created successfully. Please log in"

    def form_valid(self, form):
        try:
            Player(user=form.save()).save()
        finally:
            return super().form_valid(form)

    def form_invalid(self, form):
        if "username" in form.errors and form.errors["username"][0].endswith("username already exists."):  # Ha!
            msg.add_message(self.request, msg.ERROR,f"Username {form.data["username"]} is taken. How about {new_username(form.data["first_name"])}?")
        return super().form_invalid(form)
    
    def get(self, request):
        return redirect("/lounge/") if self.request.user.is_authenticated else super().get(request)

class SignIn(SuccessMessageMixin, LoginView):
    template_name = "signin.html"
    success_message = "Signin successful!"
    redirect_authenticated_user = True
    
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            player = self.request.user.player
            player.logged_in = True
            player.score = 0
            player.save()
        return super().dispatch(*args, **kwargs)


class SignOut(LoginRequiredMixin, LogoutView):
    template_name = "signed_out.html"
    LogoutView.http_method_names.append("get")  # HA!

    def post(self, request):
        player = request.user.player
        if player.game:
            return self.get(request)
        player.logged_in = False
        player.save()
        return super().post(request)
    
    def get(self, request):
        if request.user.player.game:
            msg.add_message(request, msg.ERROR, "You cannot sign out now. You are in a game")
            return redirect("/lounge/")
        return render(request, "signout.html")

# Maybe define a class that inherits UserPassesTestMixin, and has redirect_url instead of raising 403
