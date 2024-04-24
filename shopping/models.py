from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    brand = models.CharField(max_length=255)
    country_code = models.CharField(max_length=255)
    price = models.FloatField()
    # use decimal instead of float to avoid rounding errors
    # always use decimal for money values
    created_date = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        try:
            return f'{self.name},{self.brand},{self.country_code},{self.price},{self.created_date}'
        except AttributeError as error:
            return "Attributes are missing"

################

class Country(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='countries')
    countryCode = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    country_name = models.TextField()

    def __str__(self):
        try:
            return f'{self.product},{self.countryCode},{self.latitude},{self.longitude},{self.country_name}'
        except AttributeError as error:
            return "Attributes are missing"

# Customer model

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    address = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email}, {self.address}'

    class Meta:
        db_table = 'customer'

        
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Customer.objects.create(user=instance)
    
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.customer.save()


# Cart model

class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='cart')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart for {self.customer.user.email} created on {self.created_date.strftime("%Y-%m-%d %H:%M:%S")}'

    def total_price(self):
        return sum(item.total_price() for item in self.cart_items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in cart of {self.cart.customer.user.email}'

    def total_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    customer = models.ForeignKey('shopping.Customer', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer},{self.created_date}'