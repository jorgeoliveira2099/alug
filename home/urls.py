from django.urls import path
from .views import pesquisa, my_logout, termosDeUso, perguntasFrequentes, home, sejaPrime


urlpatterns = [
    path('', home, name='home'),
    path('logout/', my_logout, name='logout'),
    path('pesquisa/', pesquisa, name='pesquisaDescricao'),
    path('termos/', termosDeUso, name='termosDeUso'),
    path('perguntas/', perguntasFrequentes, name='perguntasFrequentes'),
    path('prime/', sejaPrime, name='sejaPrime'),



]