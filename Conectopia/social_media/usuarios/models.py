from djongo import models
# Create your models here.
class Usuarios(models.Model):
    _id = models.ObjectIdField()
    nombre = models.CharField(max_length=500)
    correo = models.CharField(max_length=500)
    fecha_nacimiento = models.DateField()
    imagen = models.CharField(max_length=500)
    contrasenna = models.CharField(max_length=500)