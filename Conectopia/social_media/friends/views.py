from django.shortcuts import render
from django.http import HttpResponse 
from usuarios.models import Usuarios

# Create your views here.

from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, JsonResponse
from friends.models import Solicitud
from usuarios.models import Usuarios

from friends.models import Amistad
from django.template.loader import render_to_string
from django.contrib import messages
from django.db.models import Q

import json
from bson import ObjectId, json_util

# Create your views here.

def listFriends(request):
    userID = request.session['userID']
    userID = userID['$oid']
    user = Usuarios.objects.get(pk=ObjectId(userID))

    # Obtener la lista de amigos del usuario en sesión
    amigos = Usuarios.objects.filter(
        Q(following__user1=user) | Q(follower__user2=user)
    ).distinct()

    return render(request, 'listFriends.html', {'user': user,'amistad': amigos})


def searchUser(request):
    query = request.GET.get('buscar_query')
    users = Usuarios.objects.all()
    if query:
        users = users.filter(nombre__icontains=query)
    userID = request.session['userID']
    userID = userID['$oid']
    user = Usuarios.objects.get(pk=ObjectId(userID))
    users = users.exclude(pk=user.pk)
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        data = []
        for user in users:
            data.append({
                'pk': str(user.pk),
                'nombre': user.nombre,
                'imagen': user.imagen,
            })
        return JsonResponse(data, safe=False)
    else:
        return render(request, 'addFriends.html', {'user': user, 'usuarios_usuarios': users})

def add_request(request):
    if request.method == 'POST':
        userID = request.session['userID']
        userID = userID['$oid']
        usuario_sesion = ObjectId(userID)
        receptor_id = request.POST.get('receptor_id')

        existe_solicitud = Solicitud.objects.filter(
            (Q(Id_emisor_id=usuario_sesion) & Q(Id_receptor_id=receptor_id)) | 
            (Q(Id_emisor_id=receptor_id) & Q(Id_receptor_id=usuario_sesion)),
            Stade__in=['Pendiente', 'Aceptada']
        ).exists()

        if existe_solicitud:
            response_data = {'success': False}
        else:
            solicitud = Solicitud(Id_emisor_id=usuario_sesion, Id_receptor_id=receptor_id, Stade='Pendiente')
            solicitud.save()
            response_data = {'success': True}

            request.session['solicitud_enviada'] = True

        return JsonResponse(response_data)

    return redirect('search')
    """if request.method == 'POST':
        userID = request.session['userID']
        userID = userID['$oid']
        usuario_sesion = ObjectId(userID)
        receptor_id = request.POST.get('receptor_id')
        solicitud = Solicitud(Id_emisor_id=usuario_sesion, Id_receptor_id=receptor_id, Stade='Pendiente')
        solicitud.save()
        response_data = {'success': True}
        
        # Guardar el estado "Pendiente" en la sesión del usuario
        request.session['solicitud_enviada'] = True
        
        return JsonResponse(response_data)
    return redirect('search')"""
    """if request.method == 'POST':
        userID = request.session['userID']
        userID = userID['$oid'] 
        usuario_sesion = ObjectId(userID)

        receptor_id = request.POST.get('receptor_id')
       
        solicitud = Solicitud(Id_emisor_id=usuario_sesion, Id_receptor_id=receptor_id, Stade='Pendiente')
        solicitud.save()
        response_data = {'success': True} # Puedes modificar esto según tus necesidades
        return JsonResponse(response_data)
    return redirect('search')"""


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