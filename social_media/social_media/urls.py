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
from usuarios import views as usuariosViews
from friends import views as friendsViews
from home import views as homeViews
from preferencias import views as preferenceViews

urlpatterns = [
    path('',usuariosViews.login),
    path('admin/', admin.site.urls),
    path('login/',usuariosViews.login),
    path('userConfiguration/',usuariosViews.userConfiguration),
    path('createUser_Preferences/',usuariosViews.preferences),
    path('listFriends/',friendsViews.listFriends),
    path('addFriends/',friendsViews.agregarBas),
    path('searchUser/', friendsViews.searchUser, name='search'),
    path('createUser/',usuariosViews.createUser),
    path('createUser_Preferences/',usuariosViews.preferences),
    path('createUser_profilePicture/',usuariosViews.profilePic),
    path('home/', homeViews.home, name='home'),
    path('createUser_profilePicture/',usuariosViews.profilePic),
    path('updatePassword/',usuariosViews.updatePassword),
    path('deleteUser/',usuariosViews.deleteUser),
    path('closeSession/',usuariosViews.closeSession),
    path('preferenceList/',preferenceViews.preferenceList)
]