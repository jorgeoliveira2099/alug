from django.urls import path
from ratings.views import avaliarSubmit, avalia, avaliacoesPendentes

urlpatterns = [
    path('avaliar/<int:idAvalia>', avalia, name='avalia'),
    path('avaliacoesPendentes/', avaliacoesPendentes, name='avaliacoes_pendentes'),
    #path('<noti_id>/delete', DeleteNotification, name='delete_notification'),
   #aqui funcionava
    #path('avaliar/<int:idAvalia>/submit', avaliarSubmit, name='avaliar_submit'),
    path('avaliar/<int:idAvalia>/submit', avaliarSubmit, name='avaliar_submit'),

]