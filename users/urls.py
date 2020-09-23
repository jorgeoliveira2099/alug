from django.urls import path

from .views import register, excluirConta, excluirContaSubmit


urlpatterns = [
    path('cadastro/', register, name='cadastro'),
    path('excluir_conta/<int:userId>/', excluirConta, name='excluirConta'),
    path('excluir_conta/<int:userId>/submit', excluirContaSubmit),

]