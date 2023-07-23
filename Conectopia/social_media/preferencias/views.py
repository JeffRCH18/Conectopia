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

# Create your views here.
def preferenceList(request):
    
    if request.method == 'GET':

        #Recover the User for the session variables. 
        userID = request.session['userID']
        userID = userID['$oid']
        user = Usuarios.objects.get(pk = ObjectId(userID))

        userPreferences = GustosUsuarios.objects.filter(idUsuario_id = userID)

        return render (request,'preferenceList.html',{
            'documentTitle':'Preference List',
            preferenceList : userPreferences
        })
