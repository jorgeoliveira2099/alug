from django.urls import path
from .views import home, my_logout, termosDeUso, perguntasFrequentes


urlpatterns = [
    path('', home, name='home'),
    path('logout/', my_logout, name='logout'),

    path('termos/', termosDeUso, name='termosDeUso'),
    path('perguntas/', perguntasFrequentes, name='perguntasFrequentes'),



]