from rest_framework.decorators import api_view
from rest_framework import views, status
from rest_framework.response import Response
import pandas
import json
from django.http import HttpResponse
from .serializer import newSerializer
from urllib.request import urlopen


class lista(views.APIView):
    def get(self, request):
        id = request.GET.get('id')
        name = request.GET.get('name')
        dfjson = getJson("http://127.0.0.1:8000/tablajson/"+id)
        df = toDf(dfjson)
        print(df.mean())
        obj = {"id": id, "name": name}
        data = newSerializer(data=obj)
        if data.is_valid():
            return Response(data.data)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


def getJson(link):
    content = urlopen(link)
    return content


def toDf(js):
    df = pandas.read_json(js)
    return df
