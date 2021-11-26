from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .form import FormCreateUser, UploadFile
from .models import Modelo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import logging
import csv
# Create your views here.


class Index(LoginRequiredMixin, generic.TemplateView):
    template_name = "index.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        context['list'] = Modelo.objects.filter(Usuario=current_user)
        return context


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


class DetailCsv(LoginRequiredMixin, DetailView):
    model = Modelo
    template_name = "Detail.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['files'] = []
        current_user = self.request.user
        archivo = Modelo.objects.get(id=self.object.id, Usuario=current_user).uploadedFile.name
        with open(archivo) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                context["files"].append(" ".join(row))
        return context


def uploadcsv(request):
    # Contexto de prueba
    current_user = request.user
    data = {"files": []}
    if "GET" == request.method:
        form = UploadFile()
        return render(request, "Upload.html",{'form': form})
    form = UploadFile(request.POST, request.FILES)
    try:
        # Corrobora que sea csv
        csv_file = request.FILES["uploadedFile"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return render(request, "Upload.html", data)
            # evita archivos grandes
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return render(request, "Upload.html", data)
        try:
            # obtiene nombre para comparacion
            fileTitle = request.POST["Nombre"]
            # Almacena la informacion en la base de datos
            if form.is_valid():
                obj = form.save(commit=False)
                obj.Usuario = current_user
                print(obj)
                obj.save()
            else:
                return render(request, "Upload.html", {'form': form})
            directory = Modelo.objects.get(Nombre=fileTitle, Usuario=current_user).uploadedFile.name
            # Lee el archivo
            with open(directory) as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    data["files"].append(" ".join(row))
        except Exception as e:
            logging.getLogger("error_logger").error()
            pass
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))
    return render(request, "Upload.html", data)
