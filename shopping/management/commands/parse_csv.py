import csv
import os
import decimal
from decimal import Decimal, InvalidOperation
from pathlib import Path
from django.db import models
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from datetime import datetime
from shopping.models import Product, Country
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Load data into the tables'

    def handle(self, *args, **options):
        try:
            Product.objects.all().delete()       
            print("tables dropped successfully")

            # open the file to read it into the database
            base_dir = Path(__file__).resolve().parent.parent.parent.parent
            try:
                with open(str(base_dir) + '/shopping/data/laptops.csv', newline='') as f:       
                    reader = csv.reader(f, delimiter=",")
                    next(reader)  # skip the header line

                    for row in reader:
                        print(row)

                        product = Product.objects.create(
                            name=row[0],
                            brand=row[2],
                            country_code=row[3],
                            price=row[11],
                        )
                        product.save()
                print("product data parsed successfully")
            except FileNotFoundError:
                print("laptops.csv file not found.")
                return  # suspend the process if file is not found.
            except Exception as error:
                print(f"An error occurred while parsing laptops.csv: {error}")
                return  # suspend the process if any other error occurs.

            Country.objects.all().delete()
            print("tables dropped successfully")
            
            # second table
            try:
                with open(str(base_dir) + '/shopping/data/lat_lng.csv', newline='') as f:
                    reader = csv.reader(f, delimiter=",")
                    next(reader)  # skip the header line
                    
                    for row in reader:
                        print(row)

                        country_Code = row[0]  
                        print(country_Code)
                        product = Product.objects.filter(country_code=country_Code).first()
                        if product:
                            print(product.id)

                            country = Country.objects.create(
                                product=product,
                                countryCode=row[0],
                                latitude=row[1],
                                longitude=row[2],
                                country_name=row[3],
                            )
                            country.save()
            
                print("longitude and latitude data parsed successfully")
            except FileNotFoundError:
                print("lat_lng.csv file not found.")
                return  
            except Exception as error:
                print(f"An error occurred while parsing lat_lng.csv: {error}")
                return

        except IntegrityError as error:
            print(f"Integrity of database error: {error}")
        except Exception as error:
            print(f"Unexpected error: {error}")
        finally:
            print("Parsing Done.")