from django.core.management.base import BaseCommand, CommandError
from django.db.models.functions.text import Left, Length
from django.db.models.query_utils import Q
from rest_framework import serializers
from catalog.models import *
import os
import json
from django.db.models.functions import Lower
from django.db.models import CharField
import time
import datetime



CharField.register_lookup(Lower)

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


qs_shop = ShopAdressModel.objects.all()
qs_prod = ProductModel.objects.all()

qs_price = PriceModel.objects.all()
qs_avail = AvailableModel.objects.all()

# # first_count = 1689


# Дублирование стоимости по магазинам
first_count = 1690
for price in qs_price:
    for shop in qs_shop:
        first_count += 1
        create_price = qs_price.get_or_create(id=first_count ,shop=shop, product=price.product, price=price.price )
        print(first_count, create_price)

two_count = 57
for product in qs_prod:

    for shop in qs_shop:
        two_count += 1
        create_avail = qs_avail.get_or_create(id=two_count, shop=shop, product=product, status="stock", quantity=1)
        print(two_count, create_avail)
