from django.test import TestCase
from django.urls import reverse
from ..forms import Dados_usuarioForm

class Dados_usuarioFormTestCase(TestCase):
    
    #TESTE DE FORMS
    def test_form_address_valid(self):
        form = Dados_usuarioForm(data={
            'cpf': '174.960.320-93',
            'nome': 'john',
            'sobrenome': 'doe',
            'data_nascimento': '10/10/2000',
            'telefone': '99 987654321',
            'cep': '57038-666',
            'cidade': 'Maceió',
            'estado': 'AL',
            'rua': 'Rua Bem-te-vi',
            'bairro': 'Jacarecica',
            'complemento': 'algum texto'
        })

        self.assertTrue(form.is_valid())
    
    def test_form_address_invalid(self):
        form = Dados_usuarioForm(data={})
        #isso não pode ser true
        self.assertTrue(form.is_valid())
