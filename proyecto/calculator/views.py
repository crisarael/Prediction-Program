from rest_framework.decorators import api_view
from rest_framework import views, status
from rest_framework.response import Response
import pandas
import json
from django.http import HttpResponse
from .serializer import newSerializer
from urllib.request import urlopen
import matplotlib.pyplot as plt
import numpy as np
from .graphs import return_graphHist, return_graphScatter, return_graphBar
from django.views import generic
from django.shortcuts import render


class lista(views.APIView):
    def get(self, request, pk):
        dfjson = getJsonLink("http://127.0.0.1:8000/tablajson/"+str(pk))
        df = toDf(dfjson)
        print(df)
        return Response(getJson(df))


def getJson(df):
    json_values = df.reset_index(drop=True).to_json(orient='records')
    data = []
    data = json.loads(json_values)
    return data


class grafica(generic.TemplateView):
    def get(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        id = request.GET.get('id')
        dfjson = getJsonLink("http://127.0.0.1:8000/tablajson/"+id)
        df = toDf(dfjson)
        df = df[["val", "TempMax", "pais"]]
        x = request.GET.get('x')
        y = request.GET.get('y')
        label = request.GET.get('label')
        labels = []
        labels = request.GET.getlist('etiquetas')
        if request.GET.get('metodo')=="Scatter":
            gp = return_graphScatter(df, x, y, label, labels)
        elif request.GET.get('metodo')=="Histogram":
            gp = return_graphHist(df, x,label, labels)
        elif request.GET.get('metodo')=="Bar":
            gp = return_graphBar(df, x, y, label, labels)
        context['graph'] = gp
        return render(request, 'plot.html', context)



def getJsonLink(link):
    content = urlopen(link)
    return content


def toDf(js):
    df = pandas.read_json(js)
    return df


def plotDf():
    plt.style.use('_mpl-gallery')
    # make data
    x = np.linspace(0, 10, 100)
    y = 4 + 2 * np.sin(2 * x)
    # plot
    fig, ax = plt.subplots()
    ax.plot(x, y, linewidth=2.0)
    ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
           ylim=(0, 8), yticks=np.arange(1, 8))
    plt.show()
