import os
from django.shortcuts import render
from django.shortcuts import redirect

import json
from bson import ObjectId, json_util
from django.http import JsonResponse
from django.core import serializers

from usuarios.models import Usuarios, Gustos,GustosUsuarios
from home.models import Publicaciones, Comentarios, Likes

# Create your views here.
def visit_home(request):
    userID = request.session['userID']
    userID = userID['$oid']
    user = Usuarios.objects.get(pk=ObjectId(userID))
    friendsRecommendation = json.loads(request.session['friendsSuggestion'])
    preferencesRecommendation = json.loads(request.session['preferenceSuggestion'])
    posiblePreferences = Gustos.objects.all()
    postList = Publicaciones.objects.all().order_by('-fecha_publicacion')

    return render(request, 'home.html',
        {
            'user': user,
            'friends':friendsRecommendation, 
            'preferenceRecommendations':preferencesRecommendation, 
            'preferencePost':posiblePreferences,
            'postList':postList
        }
    )

def create_post(request):

    #Get user information
    userID = request.session['userID']
    userID = userID['$oid']
    user = Usuarios.objects.get(pk=ObjectId(userID))

    #Recover the information from the front end. 
    txtBody = request.POST.get('txtPost')
    txtPreference = request.POST.get('txtPreference')

    print(txtBody)
    print(txtPreference)

    #get the preference related to the post
    preference = Gustos.objects.get(pk = ObjectId(txtPreference))

    #Save the value of the form
    newPost = Publicaciones(
        usuario = user, 
        contenido = txtBody, 
        preferencia = preference
    )

    newPost.save()

    #Create image path and save the image
    try: 
        image = request.FILES['txtPostImage']

        path = 'social_media\static_shared\shared_images\post_' + str(newPost.pk) + '.png'

        with open(path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
        
        newPost.imagen = 'shared_images/post_' + str(newPost.pk) + '.png'   
        newPost.save()
    except:
        return redirect(visit_home)

    #return basic view
    return redirect(visit_home)

def update_post(request):

    #Get user information
    userID = request.session['userID']
    userID = userID['$oid']
    user = Usuarios.objects.get(pk=ObjectId(userID))

    #Get the post
    updatePost = request.POST.get('txtIdPost')
    updatePost = Publicaciones.objects.get(pk = ObjectId(updatePost))

    #Get the new preference
    txtPreference = request.POST.get('txtUpdatePostPreference')
    preference = Gustos.objects.get(pk = ObjectId(txtPreference))

    #Update the post
    updatePost.contenido = request.POST.get('txtUpdatePost')
    updatePost.preferencia = preference
    updatePost.save()

    try: 
        image = request.FILES['txtUpdatePostImage']

        path = 'social_media\static_shared\shared_images\post_' + str(request.POST.get('txtIdPost')) + '.png'

        with open(path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
        
        updatePost.imagen = 'shared_images/post_' + str(request.POST.get('txtIdPost')) + '.png'   
        updatePost.save()
    except:
        return redirect(visit_home)

    #return basic view
    return redirect(visit_home)

def delete_post(request):
    
    #Get the post
    updatePost = request.POST.get('txtIdDeletePost')
    updatePost = Publicaciones.objects.get(pk = ObjectId(updatePost))
    
    #Try to delete the photo related to the post
    path = 'social_media\static_shared\shared_images\post_' + str(request.POST.get('txtIdDeletePost')) + '.png'

    if os.path.exists(path):
        os.remove(path)

    updatePost.delete()
    return redirect(visit_home)

def post_comment(request):
    
    #Get the post
    updatePost = request.POST.get('txtIdPostComment')
    updatePost = Publicaciones.objects.get(pk = ObjectId(updatePost))

    #Get user information
    userID = request.session['userID']
    userID = userID['$oid']
    user = Usuarios.objects.get(pk=ObjectId(userID))

    newComment = Comentarios(
        usuario = user,
        Publicacion = updatePost,
        comentario = request.POST.get('txtpostComment')
    )

    newComment.save()
    return redirect(visit_home)

def get_comentarios(request):
    
    #Get the comments related to a post
    postID = request.GET.get('postID')
    comments = Comentarios.objects.filter(Publicacion=ObjectId(postID)).select_related('usuario')
    comments_list = []

    for comment in comments:
        comment_data = {
            'id': str(comment.pk),
            'comentario': comment.comentario,
            'usuario': {
                'id': str(comment.usuario.pk),
                'nombre': comment.usuario.nombre,
                'imagen': comment.usuario.imagen,
            }
        }
        comments_list.append(comment_data)

    return JsonResponse(comments_list, safe=False)