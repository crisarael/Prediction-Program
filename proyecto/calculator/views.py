from rest_framework import views
from rest_framework.response import Response
import pandas
import json
from urllib.request import urlopen
from urllib import request
from .graphs import return_graphHist, return_graphScatter, return_graphBar
from django.views import generic
from django.shortcuts import render


# Retorna un json modificado
class lista(views.APIView):
    def get(self, request, pk):
        dfjson = getJsonLink("http://127.0.0.1:8000/tablajson/"+str(pk))
        df = toDf(dfjson)
        # Codigo para modificar el json
        print(df)
        return Response(getJson(df))


# Vista encargada de graficar
class grafica(generic.TemplateView):
    def get(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        id = request.GET.get('id')
        dfjson = getJsonLink("http://127.0.0.1:8000/tablajson/"+id)
        df = toDf(dfjson)
        x = request.GET.get('x')
        y = request.GET.get('y')
        label = request.GET.get('label')
        labels = []
        labels = request.GET.getlist('etiquetas')
        if labels == [''] and label!='':
            labels = df[label].unique()
        elif labels == ['']:
            labels = []
        print(labels)
        if request.GET.get('metodo') == "Scatter":
            gp = return_graphScatter(df, x, y, label, labels)
        elif request.GET.get('metodo') == "Histogram":
            gp = return_graphHist(df, x, label, labels)
        elif request.GET.get('metodo') == "Bar":
            gp = return_graphBar(df, x, y)
        context['graph'] = gp
        return render(request, 'plot.html', context)


# Funciones de ayuda
def getJson(df):
    json_values = df.reset_index(drop=True).to_json(orient='records')
    data = []
    data = json.loads(json_values)
    return data


def getJsonLink(link):
    token = "Token a6f0f9798905aea3de742b3a10a2616c268d47ca"
    pet = request.Request(link)
    pet.add_header("Authorization", token)
    content = urlopen(pet)
    return content


def toDf(js):
    df = pandas.read_json(js)
    return df
