from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.http import Http404
from shopping.models import Product, Country


def latLng(request, id): 
    product = get_object_or_404(Product, id=id)
    countries = product.countries.all()
    return render(request, 'shopping/lat_lng.html', {'product': product, 'countries': countries})
