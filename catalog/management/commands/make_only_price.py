"""
Единая стоимость по магазинам
+ добавить единое наличие
"""

from django.core.management.base import BaseCommand
from catalog.models import *



class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


category = CategoryModel.objects.all()
queryset = ProductModel.objects.filter(activated=True)
prices_qs = PriceModel.objects.all()

currency = {
    "CNY": 8.82,
    "USD": 95,
    "EUR": 95,
    "RUB": 1
}


count = 0

for product in queryset:
    count += 1
    prod = { "id": None, "name": None, "only_price": None, "price": None }

    if product.only_price_status:
        prod["id"] = product.id
        prod["name"] = product.name
        prod["price"] = int(product.only_price * currency[product.currency])
        prod["only_price"] = True

    else:
        price_qs = prices_qs.filter(product = product.id)
        prod["id"] = product.id
        prod["name"] = product.name
        prod["price"] = int(price_qs[0].price * currency[price_qs[0].currency])
        prod["only_price"] = False



    print(f'{ count }/{ prod["id"] }. { prod["price"] } { prod["only_price"] } { prod["name"][0:50]}... ')

    if product.only_price_status == False:
        success = queryset.filter(id=prod["id"]).update(only_price=prod["price"], only_price_status=True)
        print(f'Перезаписали: {prod["id"]} {success}')  


    







