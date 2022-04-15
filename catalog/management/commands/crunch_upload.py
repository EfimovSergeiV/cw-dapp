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



date_name = datetime.datetime.now().date()
filename =  'uploads/' + str(date_name) + '.json'
qs_shop = ShopAdressModel.objects.all()
qs_prod = ProductModel.objects.all()

qs_price = PriceModel.objects.all()
qs_avail = AvailableModel.objects.all()

count = 0

with open(filename) as file:
    json_data = json.load(file)

    for prod_upload in json_data:

        # log_str = str(prod_upload['shop_UID']) + ' ' + str(prod_upload['prod_UID']) + ' ' + str(prod_upload['price']) + ' ' + str(prod_upload['currency']) + ' ' + str(prod_upload['quantity'])

        shop = qs_shop.filter(UID=prod_upload['shop_UID']).exists()
        if shop:
            shop = qs_shop.filter(UID=prod_upload['shop_UID'])

            prod = qs_prod.filter(UID=prod_upload['prod_UID']).exists()
            if prod:
                prod = qs_prod.filter(UID=prod_upload['prod_UID'])

                currency = 'RUB' if prod_upload['currency'] not in ('RUB', 'EUR', 'USD') else prod_upload['currency']
                prod_status = 'order' if prod_upload['quantity'] == 0 else 'stock'

                price_update = qs_price.filter(product=prod[0], shop=shop[0]).update(
                    # shop_id= shop.id,
                    # shop = shop,
                    # product = prod,
                    # product_id = prod.id,
                    price = prod_upload['price'],
                    currency = currency,
                    )
                avail_update = qs_avail.filter(product=prod[0], shop=shop[0]).update(
                    # shop_id= shop.id,
                    # shop = shop,
                    # product = prod,
                    # product_id = prod.id,
                    status = prod_status,
                    quantity = prod_upload['quantity'],
                    )

                count += 1

                print(
                     '/Запись ' + str(count),
                    # '/СТАТУС СТОИМОСТИ:\t' + str(price_update),
                    # '/СТАТУС НАЛИЧИЯ:\t' + str(avail_update),
                    '\n/ТОВАР:\t' + prod[0].name,
                    '/МАГАЗИН:\t' + shop[0].adress,
                    '\n'
                    )