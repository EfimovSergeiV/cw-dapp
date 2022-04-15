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


# КАТЕГОРИИ ПОД ЗАКАЗ / 8, 90, 11, 9,106
count = 0

for product in qs_prod:
    if product.category_id in [8, 9, 11, 90, 106 ]:
        if product.brand_id != 6:
            count += 1
            write = qs_avail.filter(product=product).update(status="order", quantity=0)
            print(
                str(count) + ') ',
                'WRITE:', write,
                product.category_id,
                product.brand_id,
                product.name
            )
            