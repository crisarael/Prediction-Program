from rest_framework import serializers
from .models import Modelo


class modeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelo
        fields = ("id", "Nombre", "Usuario")
