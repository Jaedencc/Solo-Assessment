from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Product


class ProductForm (forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name','brand','country_code','price',)