import requests
from django.conf import settings
from django.contrib import messages as msg
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sessions.backends.db import SessionStore as x
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from helpers import handle_error


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """Token generator for account activation."""

    def _make_hash_value(self, user, timestamp):
        """Generate hash value for token."""
        return str(user.pk) + str(timestamp) + str(user.is_active)


account_activation_token = AccountActivationTokenGenerator()


def send_confirmation_email(new_user, scheme, host):
    """Send account activation email."""
    uidb64 = urlsafe_base64_encode(force_bytes(new_user.pk))
    token = account_activation_token.make_token(new_user)
    activate_url = f"{scheme}://{host}/activate/{uidb64}/{token}/"
    context = {"user": new_user, "activate_url": activate_url}
    email_html_message = render_to_string(
        "registration/account_activation_email.html", context
    )
    email = EmailMessage(
        subject="Wooden: Activate Your Account",
        body=email_html_message,
        to=[new_user.email],
    )
    email.content_subtype = "html"
    email.send(fail_silently=False)


class NeedsConfirmationMixin:
    """Will send email to user and ask them to verify"""

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        data = request.POST
        username = data.get("username")
        email = data.get("email")
        user = None

        # Prioritize email when it's available (it's what the person should use most times?)
        if email is not None:
            try:
                user = User.objects.get(email=email)
            except Exception as e:
                pass

        # Then try the username
        if user is None and username is not None:
            try:
                user = User.objects.get(username=username)
            except Exception as e:
                pass

        if not user:  # How did we get here?
            return response

        email = user.email
        if not email:
            # Did not go through normal sign up - probably fast sign in
            msg.add_message(
                request,
                msg.INFO,
                "You don't have an account yet, please create a new one with another username",
            )

            return redirect("/signup/")  # should have come from here

        if not user.is_active:  # The case this was made for, not yet confirmed
            send_confirmation_email(user, request.scheme, request.get_host())
            msg.add_message(
                request,
                msg.INFO,
                "You have not yet verified your account, a confirmation email has just been sent",
            )
            return redirect("/signin/")  # Should have come from here

        # User is active, and is not temporary
        return response


class NotLoginRequiredMixin(AccessMixin):
    """Redirect user if user is authenticated.
    Mixin for Not login required
    """

    redirect_where = "/lounge/"

    def dispatch(self, request, *args, **kwargs):
        """Dispatch method for the class."""
        response = super().dispatch(request, *args, **kwargs)
        if request.user.is_authenticated:
            return redirect(self.redirect_where)
        return response


class RecaptchaFormMixin:
    """Mixin to add reCAPTCHA verification to form views."""

    recaptcha_error_message = "Complete the reCAPTCHA."

    def form_valid(self, form):
        """Validate form and verify reCAPTCHA."""
        recaptcha_token = self.request.POST.get("g-recaptcha-response")
        if not (recaptcha_token and verify_recaptcha(recaptcha_token)):
            msg.add_message(self.request, msg.ERROR, self.recaptcha_error_message)
            return super().form_valid(form)
            return self.form_invalid(form)
        return super().form_valid(form)


def verify_recaptcha(token):
    """Verify recaptcha token."""
    try:
        response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": settings.RECAPTCHA_SECRET_KEY,
                "response": token,
            },
        )
        return response.json().get("success", False)
    except Exception as error:
        handle_error(error)
        return False
