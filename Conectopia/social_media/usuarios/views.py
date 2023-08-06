from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

#Data manipulation
import json
from bson import json_util
from bson import ObjectId

#Import models related to Django
from usuarios.models import Usuarios
from usuarios.models import Gustos
from usuarios.models import GustosUsuarios

#Import decoratorsfrom decorators import session_filter_required
from usuarios.decorators import session_filter_required

#Import data related to the user
import usuarios.loadStadistics as ls

#Import new views
from home.views import visit_home

#Data Models
from friends.models import  Solicitud,Amistad
from home.models import Publicaciones

# Create your views here.
def login (request):
    #Execute when the page is going to be load 
    if request.method == 'GET':
        return render(request,'login.html',{
            'documentTitle':'Log In'
        })
    
    #The user complete the form
    if request.method == 'POST':

        txtUser = request.POST.get('txtUser')
        txtPassword = request.POST.get('txtPassword')

        try: 
            userDB = Usuarios.objects.get(correo = txtUser, contrasenna = txtPassword)
            
            
            if(userDB == None):
                return render(request, 'login.html',{
                    'documentTitle':'Log In',
                    'notification':'User ' + txtUser + ' not found'
                })
            else:

                request.session['userID'] = json.loads(json_util.dumps(userDB.pk))
                request.session['friendsSuggestion'] = ls.getNewFriendsSuggestion(userDB.pk)
                request.session['preferenceSuggestion'] = ls.getNewPreferencesSuggestion(userDB.pk)

                return redirect(visit_home)
        except Exception as e:
            print(e)
            return render(request, 'login.html',{
                'documentTitle':'Log In',
                'notification':'User ' + txtUser + ' not found'
            })

@session_filter_required()
def userConfiguration(request):

    #Execute when the page is going to be load
    if request.method == 'GET':

        #Get the user that is log in the web page
        #Required for all the views
        userID = request.session['userID']
        userID = userID['$oid']
        user = Usuarios.objects.get(pk = ObjectId(userID))   
        friendsRecommendation = json.loads(request.session['friendsSuggestion'])
        preferencesRecommendation = json.loads(request.session['preferenceSuggestion'])
        solicitudes_pendientes = Solicitud.objects.filter(Id_receptor = user, Stade = 'Pendiente').count()
        user_post = Publicaciones.objects.filter(usuario = user).count()
        user_following = Amistad.objects.filter(user1 = user).count()
        user_follower = Amistad.objects.filter(user2 = user).count()

        return render(request,'userConfiguration.html',{
            'documentTitle':'User Configuration',
            'user':user,
            'friends':friendsRecommendation,
            'preferenceRecommendations':preferencesRecommendation,
            'solicitudes_pendientes':solicitudes_pendientes,
            'user_post':user_post,
            'user_following':user_following,
            'user_follower':user_follower,
        })
    
    if request.method == 'POST':
        
        #Recover the User for the session variables. 
        userID = request.session['userID']
        userID = userID['$oid']
        user = Usuarios.objects.get(pk = ObjectId(userID))

        #Modify the user information with the name of the users. 
        user.nombre = request.POST.get('txtFullName')
        user.correo = request.POST.get('txtEmail')
        user.user_description = request.POST.get('txtDescription')


        # -- Validate if the user change the profile picture and save it. --

        picture_field = request.FILES.get('txtImage')

        if picture_field is not None: 

            #Recover the image
            image = request.FILES['txtImage']
        
            #Create the path where the image is going to be store
            path = 'social_media\static_shared\shared_images\profilepic_' + userID + '.png'

            #Store the image in the selected folder
            with open(path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            user.imagen = 'shared_images/profilepic_' + userID + '.png' 

        user.save()

        return redirect(userConfiguration)

@session_filter_required()
def updatePassword(request):
    if request.method == 'POST':

        #Recover the User for the session variables. 
        userID = request.session['userID']
        userID = userID['$oid']
        user = Usuarios.objects.get(pk = ObjectId(userID))

        #Modifyt the user password
        user.contrasenna = request.POST.get('txtNewPassword')
        user.save()

        return redirect(userConfiguration)

@session_filter_required()
def deleteUser(request):
    if request.method == 'POST':
        
        #Recover the User for the session variables. 
        userID = request.session['userID']
        userID = userID['$oid']
        user = Usuarios.objects.get(pk = ObjectId(userID))

        #Delete the user
        user.delete()
        del request.session['userID']

        return redirect(login)

def createUser(request):
    #Load the page when the user press the create user button. 
    if request.method == 'GET':
        return render(request,'createUser.html',{
            'documentTitle':'Create User'
        })
    
    #Create a new user when the user complete the form
    if request.method == 'POST':

        #Populate all the values from the request. 
        txtFullName = request.POST.get('txtFullName')
        txtEmail = request.POST.get('txtEmail')
        txtDate = request.POST.get('txtDate')
        txtDescription = request.POST.get('txtDescription')
        txtPassword = request.POST.get('txtPassword')
        txtPasswordConfirmation = request.POST.get('txtPasswordConfirmation')

        if txtPassword == txtPasswordConfirmation:

            #Create the user
            user = Usuarios(
                nombre = txtFullName,
                correo = txtEmail,
                fecha_nacimiento = txtDate,
                user_description = txtDescription,
                imagen = None,
                contrasenna = txtPassword
            )

            user.save()

            request.session['userID'] = json.loads(json_util.dumps(user.pk))

            return redirect(preferences)
        
        else:
            return render(request,'createUser.html',{
                'notification':'The password confirmation does not match'
            })

@session_filter_required()
def preferences(request):
    if request.method == "GET":

        #Get the full list of possible preferences that the user could select. 
        context = {'preferences' : Gustos.objects.all()}

        #Return the list with the information of the table. 
        return render(request,'createUser_preferences.html',context)

    if request.method == "POST": 

        #Get the selected values for the user and the user id
        preferences = request.POST.getlist('preferences')
        userID = request.session['userID']
        userID = userID['$oid']

        user = Usuarios.objects.get(pk = ObjectId(userID))   

        #Navigate for each selected item and create a new line in the database. 
        for preference in preferences:

            preferenceDB = Gustos.objects.filter(_id = ObjectId(preference)).first()

            preferenceUserDB = GustosUsuarios(
                idUsuario = user,
                idGusto = preferenceDB
            )

            preferenceUserDB.save()
        
        return redirect(profilePic)

@session_filter_required()
def profilePic(request):

    #Execute when the page is going to be load
    if request.method == 'GET':
        return render(request,'createUser_profilePic.html',{
            'documentTitle':'Create User - ProfilePic'
        })
    
    if request.method == 'POST':

        #Recover user information
        userID = request.session['userID']
        userID = userID['$oid']

        #Recover the image
        image = request.FILES['profilePic']

        #Create the path where the image is going to be store
        path = 'social_media\static_shared\shared_images\profilepic_' + userID + '.png'

        #Store the image in the selected folder
        with open(path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        #Add the new path to the user information in the database
        user = Usuarios.objects.get(pk = ObjectId(userID))
        user.imagen = 'shared_images/profilepic_' + userID + '.png'   
        user.save()

        
        return redirect(visit_home)

@session_filter_required()
def closeSession(request):
    request.session.clear()
    return redirect(login)