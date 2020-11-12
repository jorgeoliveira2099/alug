from django.urls import path
from .views import home, my_logout, termosDeUso, perguntasFrequentes
from products.views import lista_products


urlpatterns = [
    path('', lista_products, name='home'),
    path('logout/', my_logout, name='logout'),

    path('termos/', termosDeUso, name='termosDeUso'),
    path('perguntas/', perguntasFrequentes, name='perguntasFrequentes'),



]