from django.db import models
from users.models import MyUser
from products.models import Product

class Chat(models.Model):
    codigoSala = models.CharField(max_length=20, unique=True)
    locador = models.ForeignKey(MyUser, null=True, blank=True, related_name='chat_locador',
                                on_delete=models.SET_NULL)
    locatario = models.ForeignKey(MyUser, null=True, blank=True, related_name='chat_locatario',
                                  on_delete=models.SET_NULL)
    nomeSala = models.CharField(max_length=200, blank=True, null=True)
    produto = models.ForeignKey(Product, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.codigoSala

class Mensagem(models.Model):
    texto = models.CharField(max_length=80)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.texto