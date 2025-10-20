from django.test import SimpleTestCase
from django.urls import reverse, resolve
from APPEstoque import views

class UrlsTestCase(SimpleTestCase):
    def test_urls_resolvem_as_views_corretas(self):
        self.assertEqual(resolve(reverse('index')).func, views.index)
        self.assertEqual(resolve(reverse('cadastro')).func, views.cadastro)
        self.assertEqual(resolve(reverse('dashboard')).func, views.dashboard)
        self.assertEqual(resolve(reverse('password')).func, views.password)
        self.assertEqual(resolve(reverse('container')).func, views.container)