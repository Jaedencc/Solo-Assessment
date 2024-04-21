from django.conf import settings
from django.db import models
from django.utils import timezone

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