from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class FormCreateUser(UserCreationForm):

    class Meta:
        model = User
        fields = [
        "username",
        "email",
        "password1",
        "password2",
        ]

    def clean_Username(self):
        username = self.cleaned_data["Username"]
        if User.objects.filter(Username=username).exists():
            raise forms.ValidationError('El nombre ya esta en uso')
        return username
