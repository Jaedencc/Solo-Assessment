from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from shopping.models import Product, Cart, Customer, CartItem, Order
from shopping.forms import SignUpForm
from shopping.views.basket import Basket

def signup(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.customer.first_name = form.cleaned_data.get('first_name')
        user.customer.last_name = form.cleaned_data.get('last_name')
        user.customer.address = form.cleaned_data.get('address')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password= password)
        login(request, user)
        return redirect('/')
    return render(request, 'signup.html', {'form': form})

def Pay(request):
    basket = Basket(request)
    user = request.user
    customer = get_object_or_404(Customer, user_id=user.id)
    order = Order.objects.create(customer=customer)
    order.refresh_from_db()
    for item in basket:
        product_item = get_object_or_404(Product, id=item['product_id'])
        cart = Cart.objects.create(product = product_item, quantity=item['quantity'])
        cart.refresh_from_db()
        cart_item = CartItem.objects.create(quantity=item['quantity'], product=product_item, cart=cart,  order = order)
    basket.clear()
    return redirect('shopping:Paysuccessful' )

def purchase(request):
    if request.user.is_authenticated:
       user = request.user
       basket = Basket(request)
       
       return render(request, 'shopping/purchase.html', {'basket': basket, 'user': user})
    else:
        return redirect('shopping:login')

def Paysuccessful(request):
    return render(request, 'shopping/pay_successful.html')