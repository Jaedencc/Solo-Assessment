from decimal import Decimal
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from shopping.models import Product
from shopping.forms import BasketAddProductForm 

class Basket(object):
    
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)      # Get basket information
        if not basket:
            basket = self.session[settings.BASKET_SESSION_ID] = {} # If basket is empty, create an empty
        self.basket = basket                                       # Set basket attribute to current basket

    def __iter__(self):
        print(f'basket: { self.basket }')                          # Iterate through products in the basket
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)      # Get product objects from the database

        basket = self.basket.copy()
        for product in products:
            basket[str(product.id)]['product'] = product           # Add product object and product id to the basket
            basket[str(product.id)]['product_id'] = product.id

        for item in basket.values():
            item['price'] = Decimal(item['price'])                 # Calculate total price for each basket item
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):                                            
        return sum(item['quantity'] for item in self.basket.values()) # Return the quantity of products in the basket

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.basket:                             # If product is not in basket, add product with its quantity and price
            self.basket[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:                                         # Override the current quantity
            self.basket[product_id]['quantity'] = quantity
        else:                                                         # Increase the quantity
            self.basket[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())

#add product to basket
@require_POST
def addProduct(request, product_id):
    try:
        basket = Basket(request)
        product = get_object_or_404(Product, id=product_id)
        form = BasketAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            basket.add(product=product,quantity=cd['quantity'],override_quantity=cd['override'])
        return redirect('shopping:basket_detail')
    except Exception as error:
        return render(request, 'error.html')

#remove product from basket
@require_POST
def removeProduct(request, product_id):
    try:
        basket = Basket(request)
        product = get_object_or_404(Product, id=product_id)
        basket.remove(product)
        return redirect('shopping:basket_detail')
    except Exception as error:
        return render(request, 'error.html')

def basketDetail(request):
    try:
        basket = Basket(request)
        for item in basket:
            item['update_quantity_form'] = BasketAddProductForm(initial={'quantity': item['quantity'],'override': True})
        return render(request, 'shopping/basket.html', {'basket': basket})
    except Exception as error:
        return render(request, 'error.html')
