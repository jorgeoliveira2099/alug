from django.db import models
from users.models import MyUser
from cpf_field.models import CPFField

class Dados_usuario(models.Model):

    cpf = cpf = CPFField('cpf', default='xxx.xxx.xxx-xx')
    nome = models.CharField(max_length=255)
    sobrenome = models.CharField(max_length=255)
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    telefone = models.CharField(max_length=12)
    cep = models.CharField(max_length=8, unique=True)    
    cidade = models.CharField(max_length=255)
    estado = models.CharField(max_length=2)
    rua = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    complemento = models.CharField(max_length=255)
    user = models.OneToOneField(MyUser, null=True, blank=True, on_delete=models.CASCADE)
    foto = models.ImageField(null=True, blank=True, verbose_name="Imagem")

    def __str__(self):
        return self.nome

    @property
    def get_photo_url(self):
        if self.foto and hasattr(self.foto, 'url'):
            return self.foto.url
        else:
            return "/static/images/user.png"
