from django.urls import path
from .views import pesquisa, my_logout, termosDeUso, perguntasFrequentes
from products.views import lista_products


urlpatterns = [
    path('', lista_products, name='home'),
    path('logout/', my_logout, name='logout'),
    path('pesquisa/', pesquisa, name='pesquisaDescricao'),
    path('termos/', termosDeUso, name='termosDeUso'),
    path('perguntas/', perguntasFrequentes, name='perguntasFrequentes'),



]