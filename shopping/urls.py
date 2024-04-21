from django.urls import path, include
import django.contrib.auth.urls
from . import views
from shopping.views import products, lat_lng

app_name = 'shopping'

urlpatterns = [
        path('', views.products.product_list, name='product_list'),
        path('product/<int:id>/countries/', views.lat_lng.latLng, name='latLng'),
        path('product/<int:id>/', views.products.product_detail, name= 'product_detail'),
        path('product_new/', views.products.product_new, name= 'product_new'),
        path('product/<int:id>/edit/', views.products.product_edit, name= 'product_edit'),
        path('product/<int:id>/delete/', views.products.product_delete, name= 'product_delete'),
        ]