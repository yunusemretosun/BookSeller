from django.urls import path , include
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.all_products, name='all_products'),
]