from django.urls import path
from .views import alterar_perfil
from users.views import excluirContaSubmit


urlpatterns = [
    path('perfil/<int:userId>/', alterar_perfil, name='perfil'),
    path('perfil/<int:userId>/submit', excluirContaSubmit),
]