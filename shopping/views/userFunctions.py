from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from shopping.models import Product, Customer
from shopping.forms import SignUpForm

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