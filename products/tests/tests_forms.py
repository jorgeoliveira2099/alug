from django.test import TestCase
from django.urls import reverse
from ..forms import ProductForm, DenunciaForm, AlugarForm
from ..models import Categoria

from unittest.mock import patch
from datetime import datetime
from unittest import mock

class ProductFormTestCase(TestCase):    
   
    @patch('django.core.files.storage.FileSystemStorage.save')
    def test_form_product_valid(self, mock_save):
        imagem = 'cv.jpeg'
        data = datetime.now()        
        categoria = Categoria.objects.create(descricao='Ferramentas')
        form = ProductForm(data={
         'nome': 'serra eletrica',
         'categoria': categoria,
         'descricao': 'nova com manual de instrucao',
         'preco': '45',
         'condicoesUso': 'nova',
         'imagem': imagem,
         'alugado': False,
         'estado':'Pernambuco',
         'cidade':'Recife',
         'date': data
        })      

        self.assertTrue(form.is_valid())
    
    def test_form_product_invalid(self):
        form = ProductForm(data={})        
        self.assertFalse(form.is_valid())

    def test_form_product_partially_valid(self):
        form = ProductForm(data={
            'nome': 'serra eletrica',
            'descricao': 'nova com manual de instrucao',
            'preco': '45',
            'condicoesUso': 'nova'
            })        
        self.assertTrue(form.is_valid())

    def test_form_product_partially_invalid(self):
        form = ProductForm(data={
            'nome': 'serra eletrica',
            'descricao': 'nova com manual de instrucao',
            'preco': '45'
            
            })        
        self.assertFalse(form.is_valid())
        

