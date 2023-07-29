from djongo import models
import datetime

# Create your models here.
class Usuarios(models.Model):
    _id = models.ObjectIdField()
    nombre = models.CharField(max_length=500)
    correo = models.CharField(max_length=500)
    fecha_nacimiento = models.DateField(default=datetime.date.today)
    user_description = models.CharField(max_length=500,default='new user')
    imagen = models.CharField(max_length=500)
    contrasenna = models.CharField(max_length=500)
    

class Gustos(models.Model):
    _id = models.ObjectIdField()
    gusto = models.CharField(max_length=500)
    imagen = models.CharField(max_length=500)

class GustosUsuarios(models.Model):
    _id = models.ObjectIdField()
    idUsuario = models.ForeignKey(Usuarios,on_delete=models.CASCADE)
    idGusto = models.ForeignKey(Gustos,on_delete=models.CASCADE)