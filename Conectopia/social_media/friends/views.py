from django.shortcuts import render
from django.http import HttpResponse
from usuarios.models import Usuarios

# Create your views here.

def listarfriends(request):
    return render(request,'listafriends.html')

def agregarBas(request):
    usuarios = Usuarios.objects.all()
    return render(request, 'agregarfriends.html', {'usuarios_usuarios': usuarios})

def buscarusuario(request):
    usuarios = Usuarios.objects.all()
    query = request.GET.get('consulta')
    if query:
        usuarios = usuarios.filter(nombre__icontains=query)
    return render(request, 'agregarfriends.html', {'usuarios_usuarios': usuarios})