from django.db import models

class Usuario(models.Model):
    usuario_id = models.AutoField(primary_key=True)   
    usuario_nome = models.CharField(max_length=30)
    usuario_email = models.CharField(max_length=30)
    usuario_senha = models.CharField(max_length=30)
    usuario_tipo = models.IntegerField()

    def __str__(self):
    	return self.usuario_nome