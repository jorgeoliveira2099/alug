from django.urls import path

from .views import register
from address.views import perfil

urlpatterns = [
    path('cadastro/', register, name='cadastro'),
    path('perfil/', perfil, name='perfil')
]