from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from APPEstoque.models import Container, Produto

User = get_user_model()


class UsuarioModelTest(TestCase):
    def test_criacao_usuario(self):
        usuario = User.objects.create_user(
            email='teste@exemplo.com',
            fullname='Usuário Teste',
            password='12345'
        )
        self.assertEqual(usuario.email, 'teste@exemplo.com')
        self.assertTrue(usuario.check_password('12345'))
        self.assertEqual(str(usuario), 'Usuário Teste')


class ContainerModelTest(TestCase):
    def setUp(self):
        self.container = Container.objects.create(
            nome_container='Freezer 01',
            status='ativo'
        )

    def test_container_criado_com_sucesso(self):
        self.assertEqual(self.container.nome_container, 'Freezer 01')
        self.assertEqual(self.container.status, 'ativo')

    def test_str_container(self):
        self.assertEqual(str(self.container), 'Freezer 01 (ativo)')


class ProdutoModelTest(TestCase):
    def setUp(self):
        self.container = Container.objects.create(
            nome_container='Freezer Principal',
            status='ativo'
        )
        self.produto = Produto.objects.create(
            container=self.container,
            nome_produto='Coxinha',
            gramagem_produto='1kg',
            status_produto='frito_congelado',
            quantidade_produto=10
        )

    def test_produto_relacionado_ao_container(self):
        self.assertEqual(self.produto.container, self.container)

    def test_str_produto(self):
        self.assertEqual(str(self.produto), 'Coxinha (1kg)')


class ViewTest(TestCase):
    def test_pagina_dashboard_requer_login(self):
        resposta = self.client.get(reverse('dashboard'))
        # se não estiver logado, deve redirecionar (302) ou proibir (403)
        self.assertIn(resposta.status_code, [302, 403])