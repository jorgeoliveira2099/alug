from django.db import models
from users.models import MyUser
from django.urls import reverse
from datetime import datetime  

class Categoria(models.Model):
    descricao = models.CharField(max_length=100, verbose_name="Descricao")

    def __str__(self):
        return self.descricao

class Product(models.Model):
    nome = models.CharField(max_length=100, verbose_name="")
    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.CASCADE)
    descricao = models.TextField(verbose_name="")
    preco = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="")
    condicoesUso = models.TextField(verbose_name="")
    imagem = models.ImageField(null=True, blank=True, verbose_name="")
    user = models.ForeignKey(MyUser, null=True, blank=True, on_delete=models.CASCADE)
    favourite = models.ManyToManyField(MyUser, related_name='favourite', blank=True)
    alugado = models.BooleanField(default=False)
    estado = models.CharField(max_length=100, default='Pernambuco')
    cidade = models.CharField(max_length=100, default='Recife')
    date = models.DateTimeField(default=datetime.now, null=True, blank=True)

    def __str__(self):
        return self.nome

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

class Alugar(models.Model):
    inicio = models.DateField(verbose_name='Inicio Aluguel')
    fim = models.DateField(verbose_name='Fim Aluguel')
    locador = models.ForeignKey(MyUser,  null=True, blank=True, related_name='user_locador', on_delete=models.SET_NULL)
    locatario = models.ForeignKey(MyUser,  null=True, blank=True, related_name='user_locatario', on_delete=models.SET_NULL)
    confirmado = models.BooleanField()
    produto = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)





class HistoricoStatus(models.Model):
    STATUS_TYPES = ((1,'Aguardando Locador'),(2,'Proposta cancelada'), (3,'Proposta aceita'), (4,'Encerrado'), (5, 'avaliado'))
 
    status = models.IntegerField(choices=STATUS_TYPES,null=True, blank=True)

    locador = models.ForeignKey(MyUser,  null=True, blank=True, related_name='historicostatus_user_locador', on_delete=models.SET_NULL)
    locatario = models.ForeignKey(MyUser,  null=True, blank=True, related_name='historicostatus_user_locatario', on_delete=models.SET_NULL)
    produto = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL)
    encerrado = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.now, null=True, blank=True)


class StatusAguardando(HistoricoStatus):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.status = 1
        super(StatusAguardando, self).save(*args, **kwargs)

class StatusCancelado(HistoricoStatus):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.status = 2
        super(StatusCancelado, self).save(*args, **kwargs)

class StatusAceito(HistoricoStatus):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.status = 3
        super(StatusAceito, self).save(*args, **kwargs)



class StatusEncerrado(HistoricoStatus):
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.status = 4
        super(StatusEncerrado, self).save(*args, **kwargs)