from django.urls import path
from .views import room, roomSubmit, exportarpdf, criarSala, criarSalaSubmit, meusChats

urlpatterns = [
   path('room/<str:room_name>/<int:userId>/', room, name='room'),
   path('room/<str:room_name>/<int:userId>/submit', roomSubmit),
   path('criarSala/<int:idLocatario>/<int:idLocador>/', criarSala, name='criarSala'),
   path('criarSala/<int:idLocatario>/<int:idLocador>/submit', criarSalaSubmit),
   path('meusChats/', meusChats, name='meusChats'),
   path('exportarpdf/<str:room_name>/<int:userId>/', exportarpdf, name='exportarpdf'),
   
   
]