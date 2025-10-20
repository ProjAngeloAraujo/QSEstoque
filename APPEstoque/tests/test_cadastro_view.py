from django.test import TestCase, Client
from django.urls import reverse
from APPEstoque.models import Usuario

class ViewCadastroTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('cadastro')

    def test_acesso_pagina_cadastro(self):
        resposta = self.client.get(self.url)
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'APPEstoque/cadastro.html')

    def test_cadastro_sucesso(self):
        dados = {
            'fullname': 'Usuário Teste',
            'email': 'teste@exemplo.com',
            'password': '12345',
            'confirm_password': '12345'
        }
        resposta = self.client.post(self.url, dados)
        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(Usuario.objects.filter(email='teste@exemplo.com').exists())

    def test_cadastro_senhas_diferentes(self):
        dados = {
            'fullname': 'Usuário Teste',
            'email': 'teste2@exemplo.com',
            'password': '12345',
            'confirm_password': '54321'
        }
        resposta = self.client.post(self.url, dados)
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Senhas não conferem!')