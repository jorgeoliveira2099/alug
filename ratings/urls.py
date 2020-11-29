from django.urls import path
from ratings.views import avaliarSubmit, avalia, avaliacoesPendentes, avaliacoesUsuario

urlpatterns = [
    path('avaliar/<int:idAvalia>', avalia, name='avalia'),
    path('avaliacoesPendentes/', avaliacoesPendentes, name='avaliacoes_pendentes'),
    path('avaliar/<int:idAvalia>/submit', avaliarSubmit, name='avaliar_submit'),
    
    path('avaliacoesUsuario/<int:idUsuario>', avaliacoesUsuario, name='avaliacoes_usuario'),
    
]