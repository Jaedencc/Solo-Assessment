from django.urls import path, include
import django.contrib.auth.urls
from . import views
from shopping.views import products, lat_lng

app_name = 'shopping'

urlpatterns = [
        path('', views.products.product_list, name='product_list'),
        path('product/<int:id>/countries/', views.lat_lng.latLng, name='latLng'),
        ]