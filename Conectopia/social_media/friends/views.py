from django.shortcuts import render
from django.http import HttpResponse 
from usuarios.models import Usuarios

# Create your views here.

from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from friends.models import Solicitud
from usuarios.models import Usuarios
from friends.models import Amistad
from django.contrib import messages
import json
from bson import ObjectId, json_util

# Create your views here.

def listFriends(request):
    return render(request,'listFriends.html')


def searchUser(request):
    if request.method == 'GET':
        userID = request.session['userID']
        userID = userID['$oid']
        user = Usuarios.objects.get(pk = ObjectId(userID))
        
        query = request.GET.get('query')
        users = Usuarios.objects.all()
        if query:
            users = users.filter(nombre__icontains=query)
        users = users.exclude(pk=user.pk)
        return render(request,'addFriends.html',{'user':user,'usuarios_usuarios': users})

def add_request(request):
    if request.method == 'POST':
        userID = request.session['userID']
        userID = userID['$oid'] 
        usuario_sesion = ObjectId(userID)

        receptor_id = request.POST.get('receptor_id')
       
        solicitud = Solicitud(Id_emisor_id=usuario_sesion, Id_receptor_id=receptor_id, Stade='Pendiente')
        solicitud.save()
        messages.success(request, 'Solicitud enviada correctamente.')
        request.session['solicitud_enviada'] = True
    return redirect('search')


def show_requests(request):
    if request.method == 'GET':
        userID = request.session.get('userID') 
        userID = userID['$oid'] 
        user = Usuarios.objects.get(pk=ObjectId(userID))
        solicitudes_pendientes = Solicitud.objects.filter(Id_receptor_id=userID, Stade='Pendiente')
        return render(request, 'listRequest.html', {'user': user, 'friends_solicitud': solicitudes_pendientes})

def delete_accept_request(request):
    if request.method == 'POST':
        solicitud_id = request.POST.get('solicitud_id')
        accion = request.POST.get('accion')
        userID = request.session.get('userID')
        userID = userID['$oid']  
        user = Usuarios.objects.get(pk=ObjectId(userID))

        if accion == 'eliminar':
            solicitud = Solicitud.objects.get(pk=ObjectId(solicitud_id))
            solicitud.delete()
            messages.success(request, 'Solicitud aceptada correctamente.')
                
        elif accion == 'aceptar':
            solicitud = Solicitud.objects.get(pk=ObjectId(solicitud_id))
            solicitud.Stade = 'Aceptado'
            amistad = Amistad.objects.create(user1=user, user2=solicitud.Id_emisor)
            amistad.save()
            solicitud.save()
            messages.error(request, 'Solicitud eliminada correctamente.')
    return redirect('show_requests')