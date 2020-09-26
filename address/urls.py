from django.urls import path
from .views import alterar_perfil


urlpatterns = [
    path('perfil/<int:userId>/', alterar_perfil, name='perfil'),
]