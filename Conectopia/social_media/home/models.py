from django.db import models

# Create your models here.
class Publicacion(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='publicaciones/', null=True, blank=True)