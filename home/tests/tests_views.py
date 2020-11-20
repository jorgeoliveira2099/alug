from django.test import TestCase
from django.urls import reverse


class HomeViewTestCase(TestCase):

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




