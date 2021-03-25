from django.contrib import admin

from .models import Category, Product

# https://medium.com/@oguzhanoyan/8-django-uygulama-g%C3%B6r%C3%BCn%C3%BCm%C3%BC-d%C3%BCzenlemek-da5aac1d745f


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['title', 'slug', 'author','price', 'in_stock', 'created', 'updated']
    list_filter = ['in_stock', 'is_active']
    list_editable = ['price', 'in_stock']

    prepopulated_fields = {'slug': ('title',)}
