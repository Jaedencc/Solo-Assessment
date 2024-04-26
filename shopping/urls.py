from django.urls import path, include
import django.contrib.auth.urls
from . import views
from shopping.views import products, lat_lng, userFunctions, basket, orders

app_name = 'shopping'

urlpatterns = [
        path('', views.products.product_list, name='product_list'),
        path('product/<int:id>/countries/', views.lat_lng.latLng, name='latLng'),
        path('product/<int:id>/', views.products.product_detail, name= 'product_detail'),
        path('product_new/', views.products.product_new, name= 'product_new'),
        path('product/<int:id>/edit/', views.products.product_edit, name= 'product_edit'),
        path('product/<int:id>/delete/', views.products.product_delete, name= 'product_delete'),

        path('accounts/', include('django.contrib.auth.urls')),
        path('signup/', views.userFunctions.signup, name='signup'),

        path('add_product/<int:product_id>/', views.basket.addProduct, name ='add_product'),
        path('remove_product/<int:product_id>/', views.basket.removeProduct, name ='remove_product'),
        path('basket_detail/', views.basket.basketDetail, name ='basket_detail'),

        path('order_list/', views.orders.order_list, name='order_list'),
        path('order/<int:id>/', views.orders.order_detail, name= 'order_detail'),

        path('payment/', views.userFunctions.Pay, name ='payment'),
        path('purchase/', views.userFunctions.purchase, name ='purchase'),

        path('brand_chart/', views.products.brand_chart, name='brand_chart'),

        path('Pay_successful/', views.userFunctions.Paysuccessful, name='Paysuccessful'),

        path('error/', views.userFunctions.page_not_found, name='error'),
        ]