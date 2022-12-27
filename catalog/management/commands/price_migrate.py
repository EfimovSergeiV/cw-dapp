"""

Мигрирование цен товаров в единое поле

"""

from django.core.management.base import BaseCommand, CommandError
from catalog.models import *
import csv, requests, json


class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


count = 0
queryset = ProductModel.objects.filter(activated=True)
prices_qs = PriceModel.objects.all()

currency = {
    "CNY": 8.82,
    "USD": 95,
    "EUR": 95,
    "RUB": 1
}





for product in queryset:
    count += 1
    
    if product.only_price_status:
        price = int(product.only_price * currency[product.currency])
        print(f"\n{ count }\nid: { product.id }\nname: { product.name }\nO: { price } TRUE")  #{ product.category_id }

    else:
        price_qs = prices_qs.filter(product = product.id)

        price = int(price_qs[0].price * currency[price_qs[0].currency])

        print(f"\n{ count }\nid: { product.id }\nname: { product.name }\nO: {price}")
