from django.db import models
from users.models import MyUser
from django.urls import reverse

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
    imagem = models.ImageField(null=True, blank=True, verbose_name="Imagem")
    user = models.ForeignKey(MyUser, null=True, blank=True, on_delete=models.CASCADE)
    favourite = models.ManyToManyField(MyUser, related_name='favourite', blank=True)

    def __str__(self):
        return self.descricao

    def get_absolute_url(self):
        return reverse('favourite_products', kwargs={'id':self.user.id})

    @property
    def get_photo_url(self):
        if self.imagem and hasattr(self.imagem, 'url'):
            return self.imagem.url
        else:
            return "/static/images/imagemNaodisponivel.png"

class Denuncia(models.Model):
    motivo = models.CharField(max_length=100, verbose_name="Motivo")
    descricao = models.TextField(verbose_name="Descrição")
    produto = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, null=True, blank=True, on_delete=models.CASCADE)






