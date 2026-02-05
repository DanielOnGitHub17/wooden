from django.contrib import messages as msg
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views import View

from helpers import make_email
from django.conf import settings

# Create your views here.


def home(request):
    # https://www.onthisday.com/date/2010/june/21 -> Scrape to get daily insights!
    return render(request, "homepage/landing.html", {"user": request.user})


def game_help(request):
    return render(request, "homepage/game_help.html", {"user": request.user})


class Support(View):
    def post(self, request):
        email = make_email(request, request.POST["issue"])
        send_mail(
            "Wooden: Support Email", email, "sender@gmail.com", settings.DEV_MAILS
        )
        msg.add_message(request, msg.INFO, "Thanks for sending a message!")
        return redirect("/support/")

    def get(self, request):
        return render(request, "homepage/support.html")


def dev(request):
    return render(request, "homepage/dev.html", {"user": request.user})
