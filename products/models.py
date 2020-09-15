from django.db import models

class Product(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome")
    categoria = models.CharField(max_length=100, verbose_name="Categoria")
    descricao = models.CharField(max_length=100, verbose_name="Descrição")
    preco = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Preço")
    condicoesUso = models.CharField(max_length=100, verbose_name="Condições de uso")

    def __str__(self):
        return self.descricao



