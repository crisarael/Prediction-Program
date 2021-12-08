from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .form import FormCreateUser, UploadFile, FormPlot
from .models import Modelo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import logging
import pandas
import json
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from urllib.request import urlopen
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from .serielized import modeloSerializer


# Vista que regresa la lista de registros de un usuario
class verModelo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user = request.user
        obj = Modelo.objects.filter(Usuario=current_user)
        data={"data": []}
        for register in obj:
            data["data"].append(modeloSerializer(register).data)
        return Response(data)


# APi que retorna el json de la tabla correspondiente al id
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lista(request, pk):
    id = pk
    table = getJson(id)
    return Response(table)


# Api que retorna el json de la tabla  publica
@api_view(['GET'])
def listaPublica(request, pk):
    id = pk
    obj = Modelo.objects.get(id=id)
    if obj.Publico is True:
        table = getJson(id)
        return Response(table)
    return Response({"data":"Error"})


# Api que borra un modelo con autorizacion del usuario
@api_view(['GET'])
@authentication_classes([SessionAuthentication])
def eliminarLista(request, pk):
    id = pk
    obj = Modelo.objects.get(id=id, Usuario=request.user)
    if obj:
        obj.delete()
        return Response({"data":"Se a eliminado con exito"})
    return Response({"data":"Error"})


# Descargar archivos(Publico)
def descargarCsvP(request, pk):
    obj = Modelo.objects.get(id=pk, Publico=True)
    filename = obj.uploadedFile.name.split('/')[-1]
    response = HttpResponse(obj.uploadedFile, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


# Descargar archivos(Autor)
@login_required
def descargarCsv(request, pk):
    current_user = request.user
    obj = Modelo.objects.get(id=pk, Usuario=current_user)
    filename = obj.uploadedFile.name.split('/')[-1]
    response = HttpResponse(obj.uploadedFile, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


# Vista que manda un get con la informacion para graficar
@login_required
def graficar(request, pk):
    context = {'list': [], 'metodo':[], 'form':[]}
    metodos = ['Scatter', 'Histogram', 'Bar']
    current_user = request.user
    context['list'] = Modelo.objects.get(id=pk, Usuario=current_user)
    context['files'] = shareTable("values", pk)
    context['titles'] = shareTable("columns", pk)
    form = FormPlot()
    context['form'] = form
    if request.method == 'POST':
        context['metodo'] = request.POST.get('metodo')
    return render(request, 'Graficar.html', context)


# Vista de prueba que genera un hijo de la tabla
@login_required
def subData(request, pk):
    data = {"files": [], "titles": []}
    dfjson = getJsonLink("http://127.0.0.1:8000/calculator/recibir/"+str(pk))
    df = toDf(dfjson)
    data['files'] = json.loads(df.reset_index(drop=True).to_json(orient='values'))
    data['titles'] = json.loads(df.reset_index(drop=True).to_json(orient='columns'))
    print(data['titles'])
    return render(request, "subData.html", data)


# Vista que borra la tabla
class BorrarCsv(LoginRequiredMixin, DeleteView):
    model = Modelo
    success_url = reverse_lazy('Index')
    login_url = "login"
    template_name = "delete.html"


# Vista principal
class Index(LoginRequiredMixin, generic.TemplateView):
    template_name = "index.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        context['list'] = Modelo.objects.filter(Usuario=current_user)
        return context


# Vista de registro
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


# Vista para editar nombre de Dataset
def editarModelo(request, pk):
    data = {"files": [], "titles": []}
    data['files'] = shareTable("values", pk)
    data['titles'] = shareTable("columns", pk)
    data['obj'] = Modelo.objects.get(id=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        obj = Modelo.objects.get(id=pk)
        obj.Nombre = name
        obj.save()
        return redirect('Detail', pk=pk)
    return render(request, 'DetailEdit.html', data)

# Vista para visualizacion de datos
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


# Vista que hace publico un csv
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


# Vista que entrega un url publico
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


# Vista para subir un archivo
@login_required
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
    return redirect("Index")


#Funciones de ayuda
def getJsonLink(link):
    content = urlopen(link)
    return content


def toDf(js):
    df = pandas.read_json(js)
    return df


def publicar(id):
    qs = Modelo.objects.get(id=id)
    if not qs.Publico:
        qs.Publico = True
    else:
        qs.Publico = False
    qs.save()


def getJson(id):
    archivo = Modelo.objects.get(id=id).uploadedFile.name
    df = pandas.read_csv(filepath_or_buffer=archivo, index_col=False)
    json_values = df.to_json(orient='records')
    data = []
    data = json.loads(json_values)
    return data


def shareTable(value, id):
    archivo = Modelo.objects.get(id=id).uploadedFile.name
    df = pandas.read_csv(archivo)
    if value == "values":
        json_values = df.reset_index(drop=True).to_json(orient='values')
    else:
        json_values = df.reset_index(drop=True).to_json(orient='columns')
    data = []
    data = json.loads(json_values)
    return data


def getTable(value, name, usuario):
    archivo = Modelo.objects.get(Nombre=name, Usuario=usuario).uploadedFile.name
    df = pandas.read_csv(archivo)
    if value == "values":
        json_values = df.reset_index(drop=True).to_json(orient='values')
    else:
        json_values = df.reset_index(drop=True).to_json(orient='columns')
    data = []
    data = json.loads(json_values)
    return data
