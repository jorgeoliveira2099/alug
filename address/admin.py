from django.contrib import admin
from .models import Dados_usuario
from django import forms


class DadosUsuarioCreateForm(forms.ModelForm):

    class Meta:
        model = Dados_usuario
        fields = ('nome', 'sobrenome', 'data_nascimento', 'cpf',   
          		  'telefone', 'cep', 'cidade', 'estado', 'rua', 
    			   'bairro', 'complemento', 'telefone' )

    def save(self, commit=True):
       
        userdata = super().save(commit=False)        
        if commit:
            userdata.save()
        return userdata
        
admin.site.register(Dados_usuario)
