"""
URL configuration for social_media project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home import views as homeViews
from usuarios import views as usuariosViews
from friends import views as friendsViews
from preferencias import views as preferenceViews

urlpatterns = [
    path('',usuariosViews.login),
    path('admin/', admin.site.urls),
    path('login/',usuariosViews.login),
    path('userConfiguration/',usuariosViews.userConfiguration),
    path('createUser_Preferences/',usuariosViews.preferences),
    path('listFriends/',friendsViews.listFriends),
    path('searchUser/', friendsViews.searchUser, name='search'),
    path('createUser/',usuariosViews.createUser),
    path('createUser_Preferences/',usuariosViews.preferences),
    path('createUser_profilePicture/',usuariosViews.profilePic),
    path('createUser_profilePicture/',usuariosViews.profilePic),
    path('updatePassword/',usuariosViews.updatePassword),
    path('deleteUser/',usuariosViews.deleteUser),
    path('closeSession/',usuariosViews.closeSession),
    path('preferenceList/',preferenceViews.preferenceList),
    path('deletePreference/',preferenceViews.eliminatePreference),
    path('addPreference/',preferenceViews.createPreference),
    path('preferenceList/',preferenceViews.preferenceList, name='preferences'),
    path('createNewPreference/',preferenceViews.createNewPreference),
    path('show_requests/', friendsViews.show_requests, name='show_requests'),
    path('add_request/', friendsViews.add_request, name='add_request'),
    path('listFriends/',friendsViews.listFriends, name='listFriends'),
    path('delete_accept_request/', friendsViews.delete_accept_request, name='delete_accept_request'),
    path('delete_friend/',friendsViews.delete_friend, name='delete-amigo'),
    path('home_view', homeViews.home_view, name='home'),
    path('eliminar/<int:publicacion_id>/', homeViews.eliminarPublicacion, name='eliminar_publicacion')

]
