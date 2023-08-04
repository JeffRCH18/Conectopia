from django.shortcuts import render, redirect, get_object_or_404
from usuarios.models import Usuarios
from home.models import Publicacion
from .forms import PublicacionForm

import json
from bson import ObjectId
# Create your views here.
def visit_home(request):

    userID = request.session['userID']
    userID = userID['$oid']
    user = Usuarios.objects.get(pk=ObjectId(userID))



    friendsRecommendation = json.loads(request.session['friendsSuggestion'])
    preferencesRecommendation = json.loads(request.session['preferenceSuggestion'])
    
    return render(request, 'home.html',{'user': user,'friends':friendsRecommendation, 'preferenceRecommendations':preferencesRecommendation})


#publicaciones
def home_view(request):
    publicaciones = Publicacion.objects.all()  # Obtiene todas las publicaciones
    return render(request, 'home.html', {'publicaciones': publicaciones})

def crearPublicacion(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        usuario_id = request.POST['usuario_id']
        descripcion = request.POST['descripcion']
        imagen = request.FILES['imagen']

        # Obtener el usuario desde el modelo Usuarios
        usuario = Usuarios.objects.get(id=usuario_id)

        # Crear la nueva publicación
        nueva_publicacion = Publicacion(
            usuario=usuario,
            descripcion=descripcion,
            imagen=imagen
        )
        nueva_publicacion.save()

        return redirect('home_view.html') 
    return render(request, 'createPost.html') 

def modificarPublicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)

    if request.method == 'POST':
        # Obtener los nuevos datos del formulario
        nueva_descripcion = request.POST['nueva_descripcion']
        nueva_imagen = request.FILES.get('nueva_imagen')

        publicacion.descripcion = nueva_descripcion
        if nueva_imagen:
            publicacion.imagen = nueva_imagen
        publicacion.save()

        return redirect('home.html')  

    context = {'publicacion': publicacion}
    return render(request, 'updatePost.html', context)  

def eliminarPublicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)

    if request.method == 'POST':
        # Eliminar la publicación
        publicacion.delete()

        return redirect('home.html')

    context = {'publicacion': publicacion}
    return render(request, 'home.html', context)