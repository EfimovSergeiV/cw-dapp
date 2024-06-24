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



prods_qs = ExtendedProductModel.objects.all()

with open(f'ptz-price.json', 'r') as file:
    data = json.load(file)


for prod in data:
    print(prod["name"], prod["price"], prod["quantity"])
    prods_qs.create(
        name=prod["name"],
        price=prod["price"],
        quantity=prod["quantity"],
        city="Петрозаводск",
        shop='ул. Заводская, д. 2',
    )