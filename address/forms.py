from django import forms
from .models import Dados_usuario



class Dados_usuarioForm(forms.ModelForm):
    class Meta:
        model = Dados_usuario
        fields = ['cpf', 'nome', 'sobrenome', 'data_nascimento', 'telefone', 'cep', 'cidade', 'estado',
                    'rua', 'bairro', 'complemento', 'foto']

