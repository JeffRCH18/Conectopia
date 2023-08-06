from django.shortcuts import render
from django.shortcuts import redirect

#Data Manipulation
import json
from bson import ObjectId
from bson import json_util

#Data Model
from usuarios.models import GustosUsuarios
from usuarios.models import Usuarios
from usuarios.models import Gustos

from friends.models import Amistad,Solicitud
from home.models import Publicaciones

import pandas as pd

# Create your views here.
def preferenceList(request):
    
    if request.method == 'GET':

        #Recover the User for the session variables. 
        userID = request.session['userID']
        userID = userID['$oid']
        user = Usuarios.objects.get(pk = ObjectId(userID))

        preferences = Gustos.objects.all()
        preferences = pd.DataFrame(list(preferences.values()))

        print(preferences)

        #Getting all the items from the data base, do some manipulation to get only the information required. 
        preferencesUser = GustosUsuarios.objects.all()
        preferencesUser = pd.DataFrame(list(preferencesUser.values()))
        preferencesUser['is_User'] = preferencesUser['idUsuario_id'].apply(str).apply(lambda x: 1 if x == userID else 0)
        preferencesUser['idUsuario_id'] = 1
        preferencesUser = preferencesUser.groupby(['idGusto_id'],as_index=False)[['idUsuario_id','is_User']].sum()

        preferenceList = pd.merge(preferences,preferencesUser,left_on='_id',right_on='idGusto_id',how='left').drop(columns={'idGusto_id'})
        preferenceList['idUsuario_id'] = preferenceList['idUsuario_id'].fillna(0)
        preferenceList['is_User'] = preferenceList['is_User'].fillna(0)
        preferenceList = preferenceList.sort_values(by = 'is_User',ascending = False)
        preferenceList['_id'] = preferenceList['_id'].apply(str)
        preferenceList = preferenceList.rename(columns = {'_id':'gustoID'})
        
        #Concert the list in a dictionary
        preferenceList = preferenceList.to_dict(orient='records')
        friendsRecommendation = json.loads(request.session['friendsSuggestion'])
        preferencesRecommendation = json.loads(request.session['preferenceSuggestion'])
        
        #Required for all the views
        solicitudes_pendientes = Solicitud.objects.filter(Id_receptor = user, Stade = 'Pendiente').count()
        user_post = Publicaciones.objects.filter(usuario = user).count()
        user_following = Amistad.objects.filter(user1 = user).count()
        user_follower = Amistad.objects.filter(user2 = user).count()

        return render (request,'preferenceList.html',{
            'documentTitle':'Preference List',
            'user':user,
            'preferenceList':preferenceList,
            'friends':friendsRecommendation,
            'preferenceRecommendations':preferencesRecommendation,
            #Required
            'solicitudes_pendientes':solicitudes_pendientes,
            'user_post':user_post,
            'user_following':user_following,
            'user_follower':user_follower,
        })

def eliminatePreference(request):

    #Recover the User for the session variables. 
    userID = request.session['userID']
    userID = userID['$oid']

    preferenceID = request.POST.get('preferenceID')
    
    gusto = GustosUsuarios.objects.filter(
        idUsuario_id = ObjectId(userID),
        idGusto_id = ObjectId(preferenceID)
    ).first() 

    gusto.delete()

    return redirect(preferenceList)

def createPreference(request):
    
    #Recover the User for the session variables. 
    userID = request.session['userID']
    userID = userID['$oid']
    user = Usuarios.objects.get(pk = ObjectId(userID))

    preferenceID = request.POST.get('preferenceID')
    preferenceID = Gustos.objects.get(pk = ObjectId(preferenceID))

    newPreference = GustosUsuarios(
        idUsuario = user, 
        idGusto = preferenceID
    )

    newPreference.save()

    return redirect(preferenceList)

def createNewPreference(request):

    #Recover the user for the session variable
    userID = request.session['userID']
    userID = userID['$oid']
    user = Usuarios.objects.get(pk = ObjectId(userID))

    newPreference = Gustos(
        gusto = request.POST.get('txtNewPreference')
    )

    newPreference.save()

    newPreferenceUser = GustosUsuarios(
        idUsuario = user,
        idGusto = newPreference
    )

    newPreferenceUser.save()

    return redirect(preferenceList)