from django.test import TestCase
from django.urls import reverse


class HomeViewTestCase(TestCase):
    
    #TESTE DE VIEWS
    def test_home_status_code_200(self):
        response = self.client.get(reverse('home'))
        self.assertEquals(response.status_code, 200)   

    def test_logout_status_code_302(self):
        response = self.client.get(reverse('logout'))
        self.assertEquals(response.status_code, 302)

    def test_pesquisa_status_code_200(self):
        response = self.client.get(reverse('pesquisaDescricao'))
        self.assertEquals(response.status_code, 200)

    def test_termos_de_uso_status_code_200(self):
        response = self.client.get(reverse('termosDeUso'))
        self.assertEquals(response.status_code, 200)

    def test_perguntas_frequentes_status_code_200(self):
        response = self.client.get(reverse('perguntasFrequentes'))
        self.assertEquals(response.status_code, 200)

    def test_login_status_code_200(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)

    #TESTE DE TEMPLATES

    def test_home_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home/home.html')
    
    def test_login_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_template(self):
        response = self.client.get(reverse('cadastro'))
        self.assertTemplateUsed(response, 'registration/register.html')
    
    
    
