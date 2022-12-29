"""

Мигрирование цен товаров в единое поле

1. Экспорт цен в таблицу с разбором стоимости валюты и общей цены

"""

from django.core.management.base import BaseCommand, CommandError
from catalog.models import *
import csv, requests, json
import xlsxwriter
import math


class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


count = 0

category = CategoryModel.objects.all()
queryset = ProductModel.objects.filter(activated=True)
prices_qs = PriceModel.objects.all()


for prod_qs in queryset.filter(brand=9).order_by('id'):
    count += 1
    new_price = (prod_qs.only_price / 100) * 10 + prod_qs.only_price

    price = new_price

    while price % 50 != 0:
        price += 1

    print(f'{ prod_qs.id }. { prod_qs.only_price } > { new_price } > { price } { prod_qs.name }')


    queryset.filter(id=prod_qs.id).update(only_price = price)

    print(f'Новая: { prod_qs.only_price }')