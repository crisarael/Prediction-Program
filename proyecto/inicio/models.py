from django.db import models
from django.contrib.auth.models import User
import os
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token


# Modelo Principal del programa el cual almacena en la base de datos
class Modelo(models.Model):
    Usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    Nombre = models.CharField(max_length=100)
    uploadedFile = models.FileField(upload_to = "UploadedFiles/")
    Hijos = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    Publico = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.Nombre)


# Trigger que genera un token de seguridad
@receiver(models.signals.post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Trigger o signal que elimina por completo el archivo
@receiver(models.signals.post_delete, sender=Modelo)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.uploadedFile:
        if os.path.isfile(instance.uploadedFile.path):
            os.remove(instance.uploadedFile.path)
