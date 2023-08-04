from django.shortcuts import render, redirect
from usuarios.models import Usuarios
from home.models import Publicacion

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


def delete_post(request, Publicacion_id):
    Publicacion = Publicacion.objects.get(pk=Publicacion_id)
    Publicacion.delete()
    return redirect('home_view')  

