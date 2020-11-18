from django.urls import path
from .views import room, roomSubmit, exportarpdf, criarSala, criarSalaSubmit, meusChats

urlpatterns = [
   path('room/<str:room_name>/', room, name='room'),
   path('room/<str:room_name>/submit', roomSubmit),
   path('criarSala/<int:idProduto>/', criarSala, name='criarSala'),
   path('criarSala/<int:idProduto>/submit', criarSalaSubmit),
   path('meusChats/', meusChats, name='meusChats'),
   path('exportarpdf/<str:room_name>/', exportarpdf, name='exportarpdf'),
   
   
]