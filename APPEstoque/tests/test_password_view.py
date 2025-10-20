from django.test import TestCase, Client
from django.urls import reverse
from APPEstoque.models import Usuario

class ViewPasswordTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('password')
        self.usuario = Usuario.objects.create_user(
            email='troca@teste.com', fullname='Troca Senha', password='antiga'
        )

    def test_troca_senha_sucesso(self):
        dados = {
            'fullname': 'Troca Senha',
            'email': 'troca@teste.com',
            'password': 'nova',
            'confirm_password': 'nova'
        }
        resposta = self.client.post(self.url, dados)
        self.assertEqual(resposta.status_code, 302)

    def test_troca_senha_usuario_inexistente(self):
        dados = {
            'fullname': 'Nao Existe',
            'email': 'x@teste.com',
            'password': '123',
            'confirm_password': '123'
        }
        resposta = self.client.post(self.url, dados)
        self.assertContains(resposta, 'Usuário não encontrado!')

    def test_troca_senha_nao_confere(self):
        dados = {
            'fullname': 'Troca Senha',
            'email': 'troca@teste.com',
            'password': 'nova',
            'confirm_password': 'diferente'
        }
        resposta = self.client.post(self.url, dados)
        self.assertContains(resposta, 'Senhas não conferem!')