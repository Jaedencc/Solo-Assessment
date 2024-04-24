from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Product


class ProductForm (forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name','brand','country_code','price',)

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=35)
    first_name = forms.CharField(max_length=35)
    last_name = forms.CharField(max_length=35)
    email = forms.EmailField(max_length=50)
    address = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 
        'address', 'first_name', 'last_name', )


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=100, initial=1)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)