from djongo import models
from usuarios.models import Usuarios

# Create your models here.
class Amistad(models.Model):
    _id = models.ObjectIdField() 
    user1 = models.ForeignKey(Usuarios, on_delete=models.CASCADE,related_name='following') 
    user2 = models.ForeignKey(Usuarios, on_delete=models.CASCADE,related_name='follower') 

class Friendship(models.Model):
    _id = models.ObjectIdField()
    Id_emisor = models.ForeignKey(Usuarios, on_delete=models.CASCADE,related_name='emisor')
    Id_receptor= models.ForeignKey(Usuarios, on_delete=models.CASCADE,related_name='receptor')
    Stade = models.CharField(max_length=20)