from django.db import models

class Chat(models.Model):
    codigoSala = models.CharField(max_length=20, unique=True)
    locador = models.CharField(max_length=50, blank=False, null=False)
    locatario = models.CharField(max_length=50, blank=False, null=False)
    nomeSala = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.codigoSala

class Mensagem(models.Model):
    texto = models.CharField(max_length=80)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return self.texto