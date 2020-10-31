from django import forms
from .models import Product, Denuncia


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['nome', 'categoria', 'descricao', 'preco', 'condicoesUso', 'imagem']

class DenunciaForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        fields = ['motivo', 'descricao']
