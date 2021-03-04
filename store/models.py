from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

# https://stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models


class Product(models.Model):

    category = models.ForeignKey(
        Category, related_name='product', on_delete=models.CASCADE)  # her urun bir kategoriye ihtiyac duyar.

    created_by = models.ForeignKey(
        User, related_name='product_creator', on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)

    def __str__(self):
        return self.title
