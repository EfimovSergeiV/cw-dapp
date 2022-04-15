from django.core.management.base import BaseCommand, CommandError
from django.db.models.aggregates import Count
from catalog.models import *

"""
    Получаем товары, стоимость которых парситься из 1С
"""


class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


prods_qs = ProductModel.objects.all()
prices_qs = PriceModel.objects.all()

unique = []


count = -1
prod = ''

for qs_price in prices_qs:
    if qs_price.verified:
        prod = str(qs_price.product)
        if prod not in unique:
            unique.append(prod)
            

for a in unique:
    count += 1
    print(str(count)+ '. \t', a)