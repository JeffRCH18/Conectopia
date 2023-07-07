from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

#Import models related to Django
from usuarios.models import Usuarios
from usuarios.models import Gustos

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

                request.session['userName'] = userDB.nombre

                return render(request,'userConfiguration.html',{
                    'documentTitle':'User Configuration'
                })
        except Exception as e:
            print(e)
            return render(request, 'login.html',{
                'documentTitle':'Log In',
                'notification':'User ' + txtUser + ' not found'
            })

def userConfiguration(request):

    #Execute when the page is going to be load
    if request.method == 'GET':
        return render(request,'userConfiguration.html',{
            'documentTitle':'User Configuration'
        })

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
                imagen = None,
                contrasenna = txtPassword
            )

            user.save()

            return redirect(preferences)
        
        else:
            return render(request,'createUser.html',{
                'notification':'The password confirmation does not match'
            })
        
def preferences(request):
    if request.method == "GET":

        context = {'preferences' : Gustos.objects.all()}

        return render(request,'createUser_preferences.html',context)

def profilePic(request):

    #Execute when the page is going to be load
    if request.method == 'GET':
        return render(request,'createUser_profilePic.html',{
            'documentTitle':'Create User - ProfilePic'
        })