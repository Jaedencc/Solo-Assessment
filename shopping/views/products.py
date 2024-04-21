from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from shopping.models import Product

def product_list(request):
    products = Product.objects.all()    
    return render(request, 'shopping/product_list.html', {'products' : products })
