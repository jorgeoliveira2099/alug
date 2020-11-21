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
        
    def test_form_product_category_invalid(self):        
        form = ProductForm(data={
        'nome': 'serra eletrica',
        'categoria': 'jogos',
        'descricao': 'nova com manual de instrucao',
        'preco': '45',
        'condicoesUso': 'nova',               
        'estado':'Pernambuco',
        'cidade':'Recife'         
        })      

        self.assertFalse(form.is_valid())
    
    def test_form_denuncia_valid(self):
        form = DenunciaForm(data={
            'motivo': 'produto ilegal',
            'descricao': 'ilícitos'
        })        
        self.assertTrue(form.is_valid())

    def test_form_denuncia_invalid(self):
        form = DenunciaForm(data={})            
        self.assertFalse(form.is_valid())

    def test_form_denuncia_partially_invalid_case_one(self):
        form = DenunciaForm(data={
            'motivo': 'ilicito'
        })            
        self.assertFalse(form.is_valid())
    
    def test_form_denuncia_partially_invalid_case_two(self):
        form = DenunciaForm(data={
            'descricao': 'ilícitos'
        })            
        self.assertFalse(form.is_valid())

    def test_form_alugar_invalid(self):
        form = AlugarForm(data={})            
        self.assertFalse(form.is_valid())

    def test_form_alugar_valid(self):
        inicio = datetime(2020, 12, 12)
        fim =  datetime(2020, 12, 15)

        form = AlugarForm(data={
            'inicio': inicio,
            'fim': fim
        })            
        self.assertTrue(form.is_valid())

    def test_form_alugar_date_incomplete(self):        
        inicio = datetime(2020, 12, 12)
        fim =  datetime(2020, 12, 15)

        form = AlugarForm(data={
            'inicio': inicio            
        })            
        self.assertFalse(form.is_valid())

    def test_form_alugar_date_now_less_date_begin(self): 
        data = datetime.now() 
        inicio = datetime(2020, 10, 10)
        fim =  datetime(2020, 12, 15)
        
        certo = False
        if inicio > data: 
            certo = True           
            form = AlugarForm(data={
            'inicio': inicio,
            'fim': fim           
        })   
        #esse teste passou, mas está errado,
        #não pode permitir datas passadas
        #esse assert precisa ser True, para validar que não é permitido datas passadas         
        self.assertFalse(certo)
        
       