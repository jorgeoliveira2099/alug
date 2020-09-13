from django.db import models


class Product(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=9, decimal_places=2)
    condicoesUso = models.CharField(max_length=100)

    def __str__(self):
        return self.descricao



