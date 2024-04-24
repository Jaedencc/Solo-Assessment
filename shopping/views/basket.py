from django.shortcuts import redirect, render, get_object_or_404
from shopping.models import Product, Cart, CartItem
from shopping.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required

@login_required
def cart_add(request, product_id):
    cart, create = Cart.objects.get_or_create(customer=request.user.customer) 
    product = get_object_or_404(Product, id=product_id) 
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        item, created = CartItem.objects.get_or_create(cart=cart, product=product) 
        if created:
            item.quantity = cd['quantity']  
        else:
            if cd['override']:
                item.quantity = cd['quantity']  
            else:
                item.quantity += cd['quantity']  
        item.save()
    return redirect('shopping:cart_detail')

@login_required
def cart_remove(request, product_id):
    cart = get_object_or_404(Cart, customer=request.user.customer)
    product = get_object_or_404(Product, id=product_id)
    item = get_object_or_404(CartItem, cart=cart, product=product)
    item.delete()
    return redirect('shopping:cart_detail')

@login_required
def cart_detail(request):

    cart, created = Cart.objects.get_or_create(customer=request.user.customer)
    return render(request, 'shopping/basket.html', {'cart': cart})