from django.shortcuts import render
from django.http import HttpResponse 
from usuarios.models import Usuarios

# Create your views here.

def listFriends(request):
    return render(request,'listFriends.html')

def agregarBas(request):
    user = Usuarios.objects.all()
    return render(request, 'addFriends.html', {'usuarios_usuarios': user})
    

def searchUser(request):
    user = Usuarios.objects.all()
    query = request.GET.get('query')
    if query:
        user = user.filter(nombre__icontains=query)
    return render(request, 'addFriends.html', {'usuarios_usuarios': user})
