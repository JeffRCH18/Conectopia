from djongo import models

# Create your models here.
class Friends(models.Model):
    _id = models.ObjectIdField()
    id_usuario1 = models.CharField(max_length=500)
    id_usuario2 = models.CharField(max_length=500)
