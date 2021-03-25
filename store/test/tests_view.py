from unittest import skip

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from store.models import Category, Product
from store.views import product_all


class TestViewResponses(TestCase):
    
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        Category.objects.create(name='Webtoon',slug='webtoon')
        User.objects.create(username='admin')
        Product.objects.create(category_id=1,title='Webtoon',created_by_id=1,
                                          slug='webtoon',price=50,image='MoonlightScluptor')

    def test_url_allowed_hosts(self):
        """
        test allowed hosts
        """
        response = self.c.get('/',HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 400)
        response = self.c.get('/',HTTP_HOST='yourdomain.com')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        """
        test product_detail response
        """
        response = self.c.get(reverse('store:product_detail', args=['webtoon']))
        self.assertEqual(response.status_code, 200)
   
    def test_category_list_url(self):
        """
        test category_list response
        """
        response = self.c.get(reverse('store:category_list', args=['webtoon']))
        self.assertEqual(response.status_code, 200)
    
    def test_homepage_html(self):
        """
        test homepage response
        """
        request = HttpRequest()
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>MangaPazar</title>' , html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_function(self):
        request = self.factory.get('/webtoon')
        response = product_all(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>MangaPazar</title>' , html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)
