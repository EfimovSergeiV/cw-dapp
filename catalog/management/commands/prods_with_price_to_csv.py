"""
Составляем таблицу стоимостей всех товаров на сайте
Идея потом обратно их туда таким же образом забивать
"""

from django.core.management.base import BaseCommand
from catalog.models import *
import csv


class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass



qs_prods = ProductModel.objects.all()



with open('prices.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'price', 'name',]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()


    for qs_prod in qs_prods:

        prices = qs_prod.prod_price.all()
        personal_price = f'{ prices[0] } { prices[0].currency}' if len(prices) > 0 else False
        price = f'{ qs_prod.only_price } { qs_prod.currency }' if qs_prod.only_price_status else personal_price

        if qs_prod.activated:
            print(f'id: { qs_prod.id }\t{ price }\t\t{ qs_prod.name }')
            writer.writerow({'id': qs_prod.id, 'price': price, 'name': qs_prod.name })
