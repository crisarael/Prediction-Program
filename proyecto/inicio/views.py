from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .form import FormCreateUser
from .models import Document
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import logging
import csv
import pandas as pd
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

class Upload(LoginRequiredMixin, generic.TemplateView):
    template_name = "Upload.html"
    login_url = "login"

def uploadcsv(request):
    #Contexto de prueba
    if Document.objects.all():
        
        data={"files" : []}
        with open('UploadedFiles/Titanic.csv') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                data["files"].append(" ".join(row))
    if "GET" == request.method:
        return render(request, "Upload.html", data)
    try:
        csv_file = request.FILES["uploadedFile"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return render(request, "Upload.html", data)
            #evita archivos grandes
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return render(request, "Upload.html", data)
        try:
            #Asigna valores a la tabla
            fileTitle = request.POST["fileTitle"]
            uploadedFile = request.FILES["uploadedFile"]
        # Almacena la informacion en la base de datos
            document = Document(
                title = fileTitle,
                uploadedFile = uploadedFile
                )
            document.save()
            documents = Document.objects.all()
        except Exception as e:
            logging.getLogger("error_logger").error()
            pass
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))
    return render(request, "Upload.html", data)
