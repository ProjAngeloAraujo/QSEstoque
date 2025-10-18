from django.test import TestCase
from APPEstoque.models import Container

class TestContainerModel(TestCase):
    def setUp(self):
        self.container = Container.objects.create(
            nome_container="Container Teste",
            status="ativo"
        )

    def test_container_criado_com_sucesso(self):
        """Verifica se o container foi criado corretamente"""
        self.assertEqual(self.container.nome_container, "Container Teste")
        self.assertEqual(self.container.status, "ativo")

    def test_str_retorna_nome_e_status(self):
        """Verifica o método __str__"""
        self.assertEqual(str(self.container), "Container Teste (ativo)")