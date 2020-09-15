from django.db import models
from users.models import MyUser


class Categoria(models.Model):
    descricao = models.CharField(max_length=100, verbose_name="Descricao")

    def __str__(self):
        return self.descricao

class Product(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome")
    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.CASCADE)
    descricao = models.CharField(max_length=100, verbose_name="Descrição")
    preco = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Preço")
    condicoesUso = models.TextField(verbose_name="Condições de uso")
    imagem = models.ImageField(upload_to='clients_photos', null=True, blank=True, verbose_name="Imagem")
    user = models.ForeignKey(MyUser, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.descricao





