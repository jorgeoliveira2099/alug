from django.db import models
from users.models import MyUser
from cpf_field.models import CPFField

class Dados_usuario(models.Model):

    cpf = cpf = CPFField('cpf', null=True, blank=True, unique=True)
    nome = models.CharField(null=True, blank=True, max_length=255)
    sobrenome = models.CharField(null=True, blank=True, max_length=255)
    data_nascimento = models.DateField(null=True, blank=True, verbose_name='Data de Nascimento')
    telefone = models.CharField(null=True, blank=True, max_length=12)
    cep = models.CharField(null=True, blank=True, max_length=10)
    cidade = models.CharField(null=True, blank=True, max_length=255)
    estado = models.CharField(null=True, blank=True, max_length=2)
    rua = models.CharField(null=True, blank=True, max_length=255)
    bairro = models.CharField(null=True, blank=True, max_length=255)
    complemento = models.CharField(null=True, blank=True ,max_length=255)
    user = models.OneToOneField(MyUser, null=False, blank=False, on_delete=models.CASCADE)
    foto = models.ImageField(null=True, blank=True, verbose_name="Imagem")

    def __str__(self):
        return self.nome

    @property
    def get_photo_url(self):
        if self.foto and hasattr(self.foto, 'url'):
            return self.foto.url
        else:
            return "/static/images/user.png"
