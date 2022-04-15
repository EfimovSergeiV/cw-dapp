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

process = 0
count0 = 0
count1 = 0

try:
    for product in qs_prod:
        for shop in qs_shop:
            process += 1 
            print(process)
            qs_filter_price = qs_price.filter(product = product, shop=shop)
            qs_filter_avail = qs_avail.filter(product = product, shop=shop)

            if len(qs_filter_price) > 1:
                count0 += 1
                print(count0,'|', len(qs_filter_price), qs_filter_price[0].id, qs_filter_price[1].id, '\t', product.name,)
                rm0 = qs_filter_price[0].delete() #0 потому что может быть без магазина
                print("STATUS DELETE: ", rm0)

            if len(qs_filter_avail) > 1:
                count1 += 1
                print(count1,'|', len(qs_filter_avail), qs_filter_avail[0].id, qs_filter_avail[1].id, '\t', product.name,)
                rm1 = qs_filter_avail[0].delete() #0 потому что может быть без магазина
                print("STATUS DELETE: ", rm1)

except KeyboardInterrupt:
    print("\nCLOSE")
