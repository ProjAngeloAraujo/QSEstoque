from django.test import TestCase, Client
from django.urls import reverse
from APPEstoque.models import Usuario

class ViewLoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('index')
        self.usuario = Usuario.objects.create_user(
            email='login@teste.com', fullname='Login Teste', password='12345'
        )

    def test_login_sucesso(self):
        resposta = self.client.post(self.url, {
            'email': 'login@teste.com',
            'password': '12345'
        })
        self.assertEqual(resposta.status_code, 302)
        self.assertRedirects(resposta, reverse('dashboard'))

    def test_login_email_incorreto(self):
        resposta = self.client.post(self.url, {
            'email': 'naoexiste@teste.com',
            'password': '12345'
        })
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'E-mail não cadastrado')

    def test_login_senha_incorreta(self):
        resposta = self.client.post(self.url, {
            'email': 'login@teste.com',
            'password': 'senhaerrada'
        })
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Senha incorreta')