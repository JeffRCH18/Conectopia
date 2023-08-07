from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd 
from usuarios.models import Usuarios

# Create your views here.

from django.shortcuts import redirect, render
from django.http import JsonResponse
from friends.models import Solicitud
from usuarios.models import Usuarios
from home.models import Publicaciones
from friends.models import Amistad
from django.contrib import messages
from django.db.models import Q

from usuarios.decorators import session_filter_required

#Import data related to the user
import usuarios.loadStadistics as ls

import json
from bson import ObjectId, json_util

# Create your views here.

def listFriends(request):
    userID = request.session['userID']
    userID = userID['$oid']
    user = Usuarios.objects.get(pk=ObjectId(userID))

    amigos = Usuarios.objects.filter(
        Q(following__user1=user) | Q(follower__user2=user)
    ).exclude(pk=user.pk).distinct()  # Agrega .distinct() para eliminar duplicados

    friendsRecommendation = json.loads(request.session['friendsSuggestion'])
    preferencesRecommendation = json.loads(request.session['preferenceSuggestion'])
    solicitudes_pendientes = Solicitud.objects.filter(Id_receptor=user, Stade='Pendiente').count()
    user_post = Publicaciones.objects.filter(usuario = user).count()
    user_following = Amistad.objects.filter(user1 = user).count()
    user_follower = Amistad.objects.filter(user2 = user).count()
    
    return render(request, 'listFriends.html',
        {'user': user, 'amistad': amigos, 'friends': friendsRecommendation,
         'preferenceRecommendations': preferencesRecommendation,
         'solicitudes_pendientes': solicitudes_pendientes, 'user_post':user_post,
         'user_following':user_following,
         'user_follower':user_follower
        })


def searchUser(request):
    query = request.GET.get('buscar_query')
    users = Usuarios.objects.all()

    if query:
        users = users.filter(nombre__icontains=query)

    userID = request.session.get('userID')
    userID = userID['$oid']  
    user = Usuarios.objects.get(pk=ObjectId(userID))

    amigos = Amistad.objects.filter(Q(user1=user) | Q(user2=user))
    amigos_user_ids = set(amigos.values_list('user1_id', flat=True)) | set(amigos.values_list('user2_id', flat=True))
    
    solicitudes_enviadas = Solicitud.objects.filter(Id_emisor=user)
    usuarios_solicitudes_enviadas_ids = set(solicitudes_enviadas.values_list('Id_receptor_id', flat=True))

    solicitudes_recibidas = Solicitud.objects.filter(Id_receptor=user)
    usuarios_solicitudes_recibidas_ids = set(solicitudes_recibidas.values_list('Id_emisor_id', flat=True))

    usuarios_solicitudes_amigos_ids = usuarios_solicitudes_enviadas_ids | usuarios_solicitudes_recibidas_ids | amigos_user_ids
    
    usuarios_amigos_ids = set(amigos_user_ids)
    
    usuarios_usuarios = users.exclude(pk=user.pk).exclude(pk__in=usuarios_amigos_ids)

    friendsCommon = json.loads(request.session['friendsSuggestion'])
    friendsRecommendation = json.loads(request.session['friendsSuggestion'])
    preferencesRecommendation = json.loads(request.session['preferenceSuggestion'])
    solicitud_pendiente = Solicitud.objects.filter(Id_receptor=user, Stade='Pendiente').count()
    user_post = Publicaciones.objects.filter(usuario = user).count()
    user_following = Amistad.objects.filter(user1 = user).count()
    user_follower = Amistad.objects.filter(user2 = user).count()

    for usuario in usuarios_usuarios:
        usuario.en_espera = usuario.pk in usuarios_solicitudes_amigos_ids

    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        data = []
        for usuario in usuarios_usuarios:
            data.append({
                'pk': str(usuario.pk),
                'nombre': usuario.nombre,
                'imagen': usuario.imagen,
                'en_espera': usuario.en_espera 
            })
        return JsonResponse(data, safe=False)
    else:
        return render(request, 'addFriends.html', 
            {'user': user, 'usuarios_usuarios': usuarios_usuarios,
             'friends':friendsRecommendation, 'preferenceRecommendations':preferencesRecommendation,
             'solicitudes_pendientes': solicitud_pendiente,
             'user_post':user_post,
             'user_following':user_following,
             'user_follower':user_follower,'como':friendsCommon
            })


def add_request(request):
    if request.method == 'POST':
        receptor_id = request.POST.get('receptor_id')
        userID = request.session.get('userID')
        userID = userID['$oid']  
        user = Usuarios.objects.get(pk=ObjectId(userID))
        receptor = Usuarios.objects.get(pk=ObjectId(receptor_id))

        if Amistad.objects.filter(Q(user1=user, user2=receptor) | Q(user1=receptor, user2=user)).exists():
           
            return JsonResponse({'success': False, 'message': 'Ya eres amigo de este usuario.'})

        if Solicitud.objects.filter(Id_emisor=user, Id_receptor=receptor, Stade='Pendiente').exists():
            
            return JsonResponse({'success': False, 'message': 'Ya tienes una solicitud de amistad pendiente para este usuario.'})

        
        solicitud = Solicitud(Id_emisor=user, Id_receptor=receptor, Stade='Pendiente')
        solicitud.save()

        return JsonResponse({'success': True, 'message': 'Solicitud de amistad enviada correctamente.'})

    return redirect('search')

def show_requests(request):
    if request.method == 'GET':
        userID = request.session.get('userID') 
        userID = userID['$oid'] 
        user = Usuarios.objects.get(pk=ObjectId(userID))
        
        solicitudes_pendientes = Solicitud.objects.filter(Id_receptor_id=user, Stade='Pendiente')
        solicitud_pendiente = Solicitud.objects.filter(Id_receptor=user, Stade='Pendiente').count()
        friendsRecommendation = json.loads(request.session['friendsSuggestion'])
        preferencesRecommendation = json.loads(request.session['preferenceSuggestion'])
        user_post = Publicaciones.objects.filter(usuario = user).count()
        user_following = Amistad.objects.filter(user1 = user).count()
        user_follower = Amistad.objects.filter(user2 = user).count()
        
        return render(request, 'listRequest.html',
            {'user': user, 'friends_solicitud': solicitudes_pendientes,
             'friends':friendsRecommendation, 'preferenceRecommendations':preferencesRecommendation,
             'solicitudes_pendientes': solicitud_pendiente,'user_post':user_post,
             'user_following':user_following,'user_follower':user_follower,
            })

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
            messages.warning(request, 'Solicitud eliminada correctamente.')
                
        elif accion == 'aceptar':
            solicitud = Solicitud.objects.get(pk=ObjectId(solicitud_id))
            solicitud.Stade = 'Aceptado'
            solicitud.save()

            if solicitud.Id_emisor != user:
                amistad_usuario_sesion = Amistad.objects.create(user1=user, user2=solicitud.Id_emisor)
                amistad_usuario_sesion.save()

                amistad_usuario_emisor = Amistad.objects.create(user1=solicitud.Id_emisor, user2=user)
                amistad_usuario_emisor.save()

                messages.success(request, 'Solicitud aceptada correctamente.')

        return redirect('show_requests')

def delete_friend(request):
    if request.method == 'POST':
        friend_id = request.POST.get('friend_id')
        userID = request.session.get('userID')
        userID = userID['$oid']  
        user = Usuarios.objects.get(pk=ObjectId(userID))
        friend = Usuarios.objects.get(pk=ObjectId(friend_id))

        amistades = Amistad.objects.filter(Q(user1=user, user2=friend) | Q(user1=friend, user2=user))

        for amistad in amistades:
            amistad.delete()

        try:
            solicitud = Solicitud.objects.get(Q(Id_emisor=user, Id_receptor=friend ) | Q(Id_emisor=friend, Id_receptor=user ))
            solicitud.delete()
        except Solicitud.DoesNotExist:
            pass

        messages.success(request, 'Amistad eliminada correctamente.')

    return redirect('listFriends')

