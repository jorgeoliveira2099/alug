from django.contrib import admin
from django.urls import path, include
from .views import room, criarSala, index


urlpatterns = [
   path('', index, name='index'),
   path('room/<str:room_name>/<int:userId>/', room, name='room'),
   path('criarSala/<int:idLocatario>/<int:idLocador>/<int:idProduto>', criarSala, name='criarSala'),

]