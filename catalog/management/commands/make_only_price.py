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
    prod = { "id": None, "name": None, "only_price": None, "price": None, "status": None }

    if product.only_price_status:
        prod["id"] = product.id
        prod["name"] = product.name
        prod["price"] = int(product.only_price * currency[product.currency])
        prod["only_price"] = True   #Служит только для вывода
        prod["status"] = product.status #Узнаём какое наличие из общих цен
        print(f'{ count }/{ prod["id"] }.\t{ prod["price"] }\t{ prod["only_price"] }\t{ prod["status"] }\t{ prod["name"][0:50]}...')

    else:
        price_qs = prices_qs.filter(product = product.id)
        prod["id"] = product.id
        prod["name"] = product.name
        prod["price"] = int(price_qs[0].price * currency[price_qs[0].currency])
        prod["only_price"] = False  #Служит только для вывода

        # Узнаём наличие из первого магазина
        price_qs = prices_qs.filter(product = product.id)
        prod["status"] = price_qs[0].status
        print(f'{ count }/{ prod["id"] }.\t{ prod["price"] }\t{ prod["only_price"] }\t{ prod["status"] }\t{ prod["name"][0:50]}...')

    
    while prod["price"] % 10 != 0:
        prod["price"] += 1


    queryset.filter(id=prod["id"]).update(only_price=prod["price"], currency="RUB", only_price_status=True, status = prod["status"])
    print(f'{ count }/{ prod["id"] }.\t{ prod["price"] }\t{ prod["only_price"] }\t{ prod["status"] }\t{ prod["name"][0:50]}...\n')

