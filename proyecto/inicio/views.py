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
import pandas
import json
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def lista(request, pk):
    id = pk
    table = getJson(id)
    return Response(table)


def getJson(id):
    archivo = Modelo.objects.get(id=id).uploadedFile.name
    df = pandas.read_csv(archivo)
    json_values = df.reset_index().to_json(orient = 'records')
    data = []
    data = json.loads(json_values)
    return data


class BorrarCsv(LoginRequiredMixin, DeleteView):
    model = Modelo
    success_url = reverse_lazy('Index')
    login_url = "login"
    template_name = "delete.html"


class BorrarDisp(LoginRequiredMixin):
    login_url = "login"

    def get(self, request, pk):
        current_user = self.request.user
        qs = Modelo.objects.get(id=pk, Usuario=current_user)
        if qs:
            qs.delete()
        return Index(render)


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
        context['titles'] = []
        current_user = self.request.user
        context['files'] = getTable("values", self.object.Nombre, current_user)
        context['titles'] = getTable("columns", self.object.Nombre, current_user)
        return context


class HacerPublico(LoginRequiredMixin, generic.TemplateView):
    login_url = "login"

    def get(self, request, pk):
        current_user = self.request.user
        qs = Modelo.objects.get(id=pk, Usuario=current_user)
        if qs.Publico:
            qs.Publico = False
        else:
            qs.Publico = True
        qs.save()
        return redirect('Share', pk=qs.id)


def publicar(id):
    qs = Modelo.objects.get(id=id)
    if not qs.Publico:
        qs.Publico = True
    else:
        qs.Publico = False
    qs.save()


class CompartirCsv(DetailView):
    model = Modelo
    template_name = "Share.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if(self.object.Publico):
            context['files'] = []
            context['titles'] = []
            context['files'] = shareTable("values", self.object.id)
            context['titles'] = shareTable("columns", self.object.id)
        return context


def shareTable(value, id):
    archivo = Modelo.objects.get(id=id).uploadedFile.name
    df = pandas.read_csv(archivo)
    if value == "values":
        json_values = df.reset_index().to_json(orient ='values')
    else:
        json_values = df.reset_index().to_json(orient ='columns')
    data = []
    data = json.loads(json_values)
    return data


def getTable(value, name, usuario):
    archivo = Modelo.objects.get(Nombre=name, Usuario=usuario).uploadedFile.name
    df = pandas.read_csv(archivo)
    if value == "values":
        json_values = df.reset_index().to_json(orient ='values')
    else:
        json_values = df.reset_index().to_json(orient ='columns')
    data = []
    data = json.loads(json_values)
    return data


def uploadcsv(request):
    # Contexto de prueba
    current_user = request.user
    data = {"files": [], "titles": []}
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
            # Lee el archivo
            data['files'] = getTable("values", fileTitle, current_user)
            data['titles'] = getTable("columns", fileTitle, current_user)
        except Exception as e:
            logging.getLogger("error_logger").error()
            pass
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))
    return render(request, "Upload.html", data)
