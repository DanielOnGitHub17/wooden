from django import forms
from register.models import Player

class SignForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ["fullname", "username", "password"]
        widgets = {
            "password": forms.PasswordInput()
        }