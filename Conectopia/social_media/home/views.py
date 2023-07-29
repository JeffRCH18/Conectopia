from typing import Any, Dict
from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Publicaciones
from usuarios.models import Usuarios

class PublicacionListView(ListView):
    model = Publicaciones
    template_name = 'home/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuarios'] = Usuarios.objects.all()
        return context