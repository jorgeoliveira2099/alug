from django.db import models
from users.models import MyUser

class Dados_usuario(models.Model):
	

    cpf = models.CharField(max_length=255, unique=True)
    nome = models.CharField(max_length=255)
    sobrenome = models.CharField(max_length=255)
    data_nascimento = models.CharField(max_length=255)
    telefone = models.CharField(max_length=255)
    cep = models.CharField(max_length=8, unique=True)    
    cidade = models.CharField(max_length=255)
    estado = models.CharField(max_length=2)
    rua = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    complemento = models.CharField(max_length=255)
    user = models.ForeignKey(MyUser, null=True, blank=True, on_delete=models.CASCADE)


 	
          
         
    def __str__(self):
        return self.nome
