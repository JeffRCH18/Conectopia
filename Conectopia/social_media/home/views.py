from django.shortcuts import render
from usuarios.models import Usuarios

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