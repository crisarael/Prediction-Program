from django.db import models
from django.contrib.auth.models import User
import os
from django.dispatch import receiver
# Create your models here.


class Modelo(models.Model):
    Usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    Nombre = models.CharField(max_length=100)
    uploadedFile = models.FileField(upload_to = "UploadedFiles/")
    Hijos = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    Publico = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.Nombre)


@receiver(models.signals.post_delete, sender=Modelo)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.uploadedFile:
        if os.path.isfile(instance.uploadedFile.path):
            os.remove(instance.uploadedFile.path)
