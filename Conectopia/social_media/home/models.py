from djongo import models
from usuarios.models import Usuarios

class Publicaciones(models.Model):
    _id = models.ObjectIdField()
    id_usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='usuario')
    fecha = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField()
    contenido = models.TextField()

class Comentarios(models.Model):
    _id = models.ObjectIdField()
    id_publicacion = models.ForeignKey()
    id_usuario = models.ForeignKey()
    contenido = models.TextField()