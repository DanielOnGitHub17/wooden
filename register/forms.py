"""Script to create forms for user registration and login"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

class EmailField(forms.EmailField):
    """Custom EmailField to check if email is already in use."""
    def validate(self, value):
        super().validate(value)
        if User.objects.filter(email=value).exists():
            raise forms.ValidationError("That email address is already associated with an account")
        return value

class SignUpForm(UserCreationForm):
    """Form for user registration."""
    username = forms.CharField(
        validators=[MinLengthValidator(3, 'Must be at least 3 characters')]
    )
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = EmailField(required=True, label="Email Address")
    class Meta:
        """Meta class for SignUpForm."""
        model = User
        fields = ["email", "first_name", "last_name", "username", "password1", "password2"]

class SignInForm(AuthenticationForm):
    """Form for user login."""
    class Meta:
        """Meta class for SignInForm."""
        model = User
        fields = ["username", "password"]