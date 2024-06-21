from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        validators=[MinLengthValidator(3, 'Must be at least 3 characters')]
    )
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password1", "password2"]

class SignInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]