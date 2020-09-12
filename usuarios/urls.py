from django.contrib import admin
from django.urls import path
from .views import listar_usuarios

urlpatterns = [
	path('listar/', listar_usuarios),
    
]
