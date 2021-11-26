from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Modelo

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


class UploadFile(forms.ModelForm):

    class Meta:
        model = Modelo
        fields = [
            "Nombre",
            "uploadedFile",
        ]

    def clean_Nombre(self):
        clave = self.cleaned_data["Nombre"]
        if Modelo.objects.filter(Nombre=clave).exists():
            raise forms.ValidationError('El nombre ya se encuentra en uso')
        return clave
