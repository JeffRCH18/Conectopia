from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

#Import models related to Django
from usuarios.models import Usuarios

# Create your views here.
def login (request):
    #Execute when the page is going to be load 
    if request.method == 'GET':
        return (render(request,'login.html'))
    
    #The user complete the form
    if request.method == 'POST':
        print(request.POST['txtUser'])
        return HttpResponse(request.POST['txtUser'])
    

def createUser(request):
    #Load the page when the user press the create user button. 
    if request.method == 'GET':
        return (render(request,'createUser.html'))
    
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

            return render(request,'createUser.html',{
                'notification':'User created'
            })
        else:
            return render(request,'createUser.html',{
                'notification':'The password confirmation does not match'
            })
