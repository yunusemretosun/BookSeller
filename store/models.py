from django.conf import settings
from django.db import models
from django.urls import reverse


# Create your models here.
class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)
    

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
    
    #verilen apptaki url e git mevcut argumani urldeki yerine koy ve bir url elde et
    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug]) 

    def __str__(self):
        return self.name

# https://stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models


class Product(models.Model):

    category = models.ForeignKey(
        Category, related_name='product', on_delete=models.CASCADE)  # her urun bir kategoriye ihtiyac duyar.

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='product_creator', on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/' , default='images/MoonlightScluptor.jpg')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)
    
    #verilen apptaki url e git mevcut argumani urldeki yerine koy ve bir url elde et
    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug]) 

    def __str__(self):
        return self.title
