import datetime
import os
import uuid
from django.shortcuts import render
from django.http import HttpResponse 
from usuarios.models import Usuarios
from models import Comentario, Publicacion, PublicacionForm
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from friends.models import Solicitud
from usuarios.models import Usuarios
from usuarios.models import Gustos
from usuarios.models import GustosUsuarios
from friends.models import Amistad
from django.template.loader import render_to_string
from django.contrib import messages
from django.db.models import Q
from usuarios.decorators import session_filter_required
import usuarios.loadStadistics as ls
import json
from bson import ObjectId, json_util
from home.models import Publicacion
from pymongo import MongoClient 




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
    userID = request.session['userID']
    userID = userID['$oid']
    user = Usuarios.objects.get(pk=ObjectId(userID))
    friendsRecommendation = json.loads(request.session['friendsSuggestion'])
    preferencesRecommendation = json.loads(request.session['preferenceSuggestion'])
    publicaciones = Publicacion.objects.all()  # Obtiene todas las publicaciones
    return render(request, 'home.html', {'publicaciones': publicaciones,'user':user,'friends':friendsRecommendation, 'preferenceRecommendations':preferencesRecommendation})


def crearPublicacion(request):
    userID = request.session['userID']
    userID = userID['$oid']
    user = Usuarios.objects.get(pk=ObjectId(userID))
    friendsRecommendation = json.loads(request.session['friendsSuggestion'])
    preferencesRecommendation = json.loads(request.session['preferenceSuggestion'])
    if request.method == 'GET':
        return render(request, 'createPost.html', {'user': user, 'friends': friendsRecommendation, 'preferenceRecommendations': preferencesRecommendation})
    
    if request.method == 'POST':
        descripcion = request.POST['descripcion']
        imagen = request.FILES['imagen']

        # Generate a unique filename for the image of the publication
        unique_filename = f"postpic_{uuid.uuid4().hex}.png"
        path = os.path.join('social_media/static_shared/shared_images/', unique_filename)

        # Save the image to the specific location
        with open(path, 'wb+') as destination:
            for chunk in imagen.chunks():
                destination.write(chunk)

        nueva_publicacion = Publicacion(
            usuario=user,
            descripcion=descripcion,
            imagen=f'shared_images/{unique_filename}' 
        )
        nueva_publicacion.save()

    return render(request, 'createpost.html')

def eliminarPublicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)

    if request.method == 'POST':
        # Eliminar la publicación
        publicacion.delete()
        context = {'publicacion': publicacion}
        return render(request, 'deletePost.html', context)
        

    context = {'publicacion': publicacion}
    return render(request, 'deletePost.html', context)

def crear_publicacion(request):
    if request.method == 'POST':
        userID = request.session['userID']
        userID = userID['$oid']
        user = Usuarios.objects.get(pk=ObjectId(userID))
        friendsRecommendation = json.loads(request.session['friendsSuggestion'])
        preferencesRecommendation = json.loads(request.session['preferenceSuggestion'])
        form = PublicacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home.html')  
    else:
        form = PublicacionForm()
    
    return render(request, 'crear_publicacion.html', {'form': form,'user':user,'friends':friendsRecommendation, 'preferenceRecommendations':preferencesRecommendation}) 

def editar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, pk=publicacion_id)
    
    if request.method == 'POST':
        form = PublicacionForm(request.POST, instance=publicacion)
        if form.is_valid():
            form.save()
            return redirect('home.html')  # Redirigir a la lista de publicaciones
    else:
        form = PublicacionForm(instance=publicacion)
    
    return render(request, 'editar_publicacion.html', {'form': form, 'publicacion': publicacion})


def mostrar_comentarios(request):
    comentarios = Comentario.objects.all()  # Obtén todos los comentarios desde la base de datos
    context = {'comentarios': comentarios}
    return render(request, 'comentarios.html', context)


def like_view(request):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['red_social']

    if request.method == 'POST':
        userID = request.session['userID']
        userID = userID['$oid']
        user = Usuarios.objects.get(pk=ObjectId(userID))
        
        likes_collection = db['likes_publicacion']
        likes_collection.update_one(
            {'user_id': str(user.id)},  
            {'$inc': {'likes': 1}},
            upsert=True
        )
        
        return redirect('home')  
    return redirect('error.html')  