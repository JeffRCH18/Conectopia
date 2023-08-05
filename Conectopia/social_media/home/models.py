from djongo import models
from usuarios.models import Usuarios, Gustos
from datetime import datetime

class Publicaciones(models.Model):
    _id = models.ObjectIdField()
    usuario = models.ForeignKey(Usuarios,on_delete=models.CASCADE)
    fecha_publicacion = models.DateField(default=datetime.now)
    imagen = models.CharField(max_length=500)
    contenido = models.CharField(max_length=500)
    preferencia = models.ForeignKey(Gustos,on_delete=models.CASCADE)

class Comentarios(models.Model):
    _id = models.ObjectIdField()
    usuario = models.ForeignKey(Usuarios,on_delete=models.CASCADE)
    Publicacion = models.ForeignKey(Publicaciones,on_delete=models.CASCADE)
    comentario = models.CharField(max_length=500)

class Likes(models.Model):
    _id = models.ObjectIdField()
    usuario = models.ForeignKey(Usuarios,on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicaciones,on_delete=models.CASCADE)



    
