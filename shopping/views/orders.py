from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from shopping.models import CartItem, Order

def order_list(request):
    try:
        orders = Order.objects.all()
        return render(request, 'shopping/order_list.html', {'orders' : orders})
    except Exception as error:
        return render(request, 'error.html')

def order_detail(request, id):
    try:
        order = get_object_or_404(Order, id=id)
        customer = order.customer
        user = get_object_or_404(User, id=customer.pk)
        cart_items = CartItem.objects.filter(order_id=order.id)
        return render(request, 'shopping/order_detail.html', {'order' : order, 'user': user, 'cart_items': cart_items})
    except Exception as error:
        return render(request, 'error.html')
