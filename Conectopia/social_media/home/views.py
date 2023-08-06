import os
from django.shortcuts import render
from django.shortcuts import redirect
from django.db.models import Q

import json
from bson import ObjectId, json_util
from django.http import JsonResponse
from django.core import serializers

from usuarios.models import Usuarios, Gustos,GustosUsuarios
from home.models import Publicaciones, Comentarios, Likes
from friends.models import Solicitud,Amistad

# Create your views here.
def visit_home(request):
    
    #Required for all the views
    userID = request.session['userID']
    userID = userID['$oid']
    user = Usuarios.objects.get(pk=ObjectId(userID))
    friendsRecommendation = json.loads(request.session['friendsSuggestion'])
    preferencesRecommendation = json.loads(request.session['preferenceSuggestion'])
    solicitudes_pendientes = Solicitud.objects.filter(Id_receptor = user, Stade = 'Pendiente').count()
    user_post = Publicaciones.objects.filter(usuario = user).count()
    user_following = Amistad.objects.filter(user1 = user).count()
    user_follower = Amistad.objects.filter(user2 = user).count()

    #Custom for this view: 
    posiblePreferences = Gustos.objects.all()
    postList = Publicaciones.objects.all().order_by('-fecha_publicacion')

    return render(request, 'home.html',
        {
            #Required
            'user': user,
            'friends':friendsRecommendation, 
            'preferenceRecommendations':preferencesRecommendation, 
            'solicitudes_pendientes':solicitudes_pendientes,
            'user_post':user_post,
            'user_following':user_following,
            'user_follower':user_follower,

            #Custom
            'preferencePost':posiblePreferences,
            'postList':postList,
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

def create_comment(request):
    
    #Get the post
    updatePost = request.GET.get('postID')
    updatePost = Publicaciones.objects.get(pk = ObjectId(updatePost))

    #Get user information
    userID = request.session['userID']
    userID = userID['$oid']
    user = Usuarios.objects.get(pk=ObjectId(userID))

    newComment = Comentarios(
        usuario = user,
        Publicacion = updatePost,
        comentario = request.GET.get('comment')
    )

    newComment.save()
    return get_comentarios(request)

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

def get_likes (request):

    #Get user ID
    userID = request.session['userID']
    userID = userID['$oid']

    #Get the likes of likes related to the post. 
    postID = request.GET.get('postID')
    postID = ObjectId(postID)

    likes = Likes.objects.filter(publicacion = postID)

    #recover all the likes related to the post
    likes_data = []
    userLiked = False

    for like in likes:

        if str(like.usuario.pk) == userID:
            userLiked = True


        likes_data.append(
            {
                "userName":like.usuario.nombre,
                "picPath":like.usuario.imagen
            }
        )

    responseData = {
        "user_liked":userLiked,
        "likes":likes_data
    }

    return JsonResponse(responseData)

def postLikes(request):
    
    #Get the comments related to a post
    postID = request.GET.get('postID')
    post = Publicaciones.objects.get(pk = ObjectId(postID))

    #Get user information
    userID = request.session['userID']
    userID = userID['$oid']
    user = Usuarios.objects.get(pk=ObjectId(userID))

    newLike = Likes(
        usuario = user,
        publicacion = post
    )

    newLike.save()

    return get_likes(request)

def dislikePost(request):
    #Get user information
    userID = request.session['userID']
    userID = userID['$oid']

    #Get the comments related to a post
    postID = request.POST.get('txtIdpostDislike')
    likes = Likes.objects.filter(publicacion = ObjectId(postID))

    for like in likes:
        if str(like.usuario.pk) == userID:
            like.delete()


    return redirect(visit_home)


    