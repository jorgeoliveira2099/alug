from django import forms
from django.forms import DateInput
from .models import Product, Denuncia, Alugar


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['nome', 'categoria', 'descricao', 'preco', 'condicoesUso', 'imagem']

class DenunciaForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        fields = ['motivo', 'descricao']

class AlugarForm(forms.ModelForm):
    class Meta:
        model = Alugar
        fields = ['inicio', 'fim' ]
        widgets = {
            'inicio': DateInput(attrs={'type':'date'}, format='%d-%m-%y'),
            'fim': DateInput(attrs={'type':'date'}, format='%d-%m-%y'),
        }

        exclude = ['user']