from django.test import TestCase, Client
from django.urls import reverse

class ViewContainerTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_pagina_container_carrega(self):
        resposta = self.client.get(reverse('container'))
        self.assertEqual(resposta.status_code, 200)
        self.assertTemplateUsed(resposta, 'APPEstoque/container.html')
