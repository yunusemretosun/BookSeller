from django.contrib.auth.models import User
from django.test import TestCase

from store.models import Category, Product


class TestCategoriesModel(TestCase):

  def setUp(self):
      self.data1 = Category.objects.create(name='Webtoon',slug='webtoon')
  
  def test_category_model_entry(self):
      """
        test category model data insertion/types/failed attributes
      """
      data = self.data1
      self.assertTrue(isinstance(data,Category))
      self.assertEqual(str(data),'webtoon')
  
  def test_category_model_entry(self):
      """
        test category model data return
      """
      data = self.data1
      self.assertEqual(str(data),'Webtoon')

class TestProductsModel(TestCase):

  def setUp(self):
       Category.objects.create(name='Webtoon',slug='webtoon')
       User.objects.create(username='admin')
       self.data1= Product.objects.create(category_id=1,title='Webtoon',created_by_id=1,
                                          slug='webtoon',price=50,image='MoonlightScluptor')