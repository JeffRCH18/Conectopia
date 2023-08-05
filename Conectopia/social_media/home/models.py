from django.db import models
from django import forms
from usuarios.models import Usuarios

class Comentario(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Publicacion(models.Model):
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='publicaciones/')
    likes = models.PositiveIntegerField(default=0)
    comentarios = models.ManyToManyField(Comentario, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

