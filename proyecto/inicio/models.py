from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Modelo(models.Model):
    Usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    Nombre = models.CharField(max_length=100)
    Ubicacion = models.CharField(max_length=30)
    Hijos = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    Publico = models.BooleanField(default=True)

    def __str__(self):
        return "{}".format(self.Store_Name)
