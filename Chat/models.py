from django.db import models
from products.models import Product

class Chat(models.Model):
    codigoSala = models.CharField(max_length=20, unique=True)
    locador = models.CharField(max_length=50, blank=False, null=False)
    locatario = models.CharField(max_length=50, blank=False, null=False)
    produto = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.codigoSala