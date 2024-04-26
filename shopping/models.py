from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Product Model

class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    brand = models.CharField(max_length=255)
    country_code = models.CharField(max_length=255)
    price = models.FloatField()
    created_date = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        try:
            return f'{self.name},{self.brand},{self.country_code},{self.price},{self.created_date}'
        except AttributeError as error:
            return "Attributes are missing"

# Country Model

class Country(models.Model):
    product = models.ForeignKey('shopping.Product', on_delete=models.CASCADE, related_name='countries')
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

# Cart Model

class Cart(models.Model):
    product = models.ForeignKey('shopping.Product', on_delete=models.CASCADE, related_name='carts')
    quantity = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product},{self.quantity},{self.created_date}'

class CartItem(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey('shopping.Product', on_delete=models.CASCADE)
    cart = models.ForeignKey('shopping.Cart', on_delete=models.CASCADE)
    order = models.ForeignKey('shopping.Order', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity},{self.product},{self.cart},{self.order},{self.created_date}'

# Order Model

class Order(models.Model):
    customer = models.ForeignKey('shopping.Customer', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer},{self.created_date}'

