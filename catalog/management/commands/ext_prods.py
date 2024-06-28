""" 

    Парсер выгрузки товаров из 1С в расширенный каталог

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
        ул.Леона Поземского, 92, Павильон 28 (рынок на Алмазной)
        пос. Неёлово, ул.Юбилейная д. 5ж
        ул.Шоссейная д.3а
        проспект Ленина д.57
        Посёлок Тихвинка 69, ТК "Город Мастеров" павильон №73
        ул. Заводская, д. 2
        

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

with open(f'psk-n.json', 'r') as file:
    data = json.load(file)


for prod in data:
    print(prod["name"], prod["price"], prod["quantity"])
    prods_qs.create(
        name=prod["name"],
        price=prod["price"],
        quantity=prod["quantity"],
        city="Псков",
        shop_id = 1,
        shop='пос. Неёлово, ул.Юбилейная д. 5ж',
    )



    # prod_qs = prods_qs.filter(name=prod["name"], shop_id = 1)

    # print(f"prod - {prod['name']} ({len(prod_qs)}) { prod_qs }")

    # if len(prod_qs) == 1:
    #     prod_qs.update(
    #         price=prod["price"],
    #         quantity=prod["quantity"],
    #         shop_id = 1,
    #         last_update = datetime.datetime.now()
    #     )