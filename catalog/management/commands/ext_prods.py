""" Парсер выгрузки товаров из 1С в расширенный каталог

    Псков, ул.Леона Поземского, 92, Павильон 28 (рынок на Алмазной)
    Псков, ул.Шоссейная д.3а
    Великие Луки, проспект Ленина д.57    
    Смоленск, ул. Посёлок Тихвинка 69, ТК "Город Мастеров" павильон №73
    Петрозаводск, ул. Заводская, д. 2


    Города:
        Псков
        Великие Луки        
        Смоленск
        Петрозаводск

    
    Магазины:
    1.    пос. Неёлово, ул.Юбилейная д. 5ж
    2.    ул.Леона Поземского, 92, Павильон 28 (рынок на Алмазной)
    3.    ул.Шоссейная д. 3а
    4.    проспект Ленина д.57
    5.    Посёлок Тихвинка 69, ТК "Город Мастеров" павильон №73
    6.    ул. Заводская, д. 2
        

"""

from django.core.management.base import BaseCommand, CommandError
from catalog.models import ExtendedProductModel
import json


class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


from time import sleep
import datetime
prods_qs = ExtendedProductModel.objects.all()

with open(f'psk-a.json', 'r') as file:
    data = json.load(file)



# # CREATE NEW PRODUCTS
for prod in data:
    print(prod["name"], prod["price"], prod["quantity"])
    prods_qs.create(
        name=prod["name"],
        price=prod["price"],
        quantity=prod["quantity"],
        city="Псков",
        shop_id = 2,
        shop='ул.Леона Поземского, 92, Павильон 28 (рынок на Алмазной)',
    )



# UPDATE PRODUCTS
# for prod in data:
#     prod_qs = prods_qs.filter(name=prod["name"], shop_id = 1)

#     print(f"prod - {prod['name']} ({len(prod_qs)}) { prod_qs }")

#     if len(prod_qs) == 1:
#         prod_qs.update(
#             price=prod["price"],
#             quantity=prod["quantity"],
#             shop_id = 1,
#             last_update = datetime.datetime.now()
#         )