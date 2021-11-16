from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .form import FormCreateUser
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


class Index(LoginRequiredMixin, generic.TemplateView):
    template_name = "index.html"
    login_url = "login"


def RegistrarUsuario(request):
    if request.method == 'POST':
        form = FormCreateUser(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            return redirect('Index')
    else:
        form = FormCreateUser()
    return render(request, 'register.html', {'form': form})
