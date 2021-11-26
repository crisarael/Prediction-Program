from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Modelo(models.Model):
    Usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    Nombre = models.CharField(max_length=100)
    uploadedFile = models.FileField(upload_to = "UploadedFiles/")
    Hijos = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    Publico = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.Nombre)


# Prueba
class Document(models.Model):
    title = models.CharField(max_length = 200)
    uploadedFile = models.FileField(upload_to = "UploadedFiles/")
    dateTimeOfUpload = models.DateTimeField(auto_now = True)
