from django.core.management.base import BaseCommand, CommandError
from catalog.models import *
import xlsxwriter, requests
from pathlib import Path

import json
import pandas as pd
from time import sleep


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass

product_qs = ProductModel.objects.all()

shops = {
    "d5af83ae-68e6-11e5-8261-c48e8f4373aa": "Петрозаводск Розница",
    "647af975-60ab-11e2-8971-10bf4871e437": "В.Луки Розница",
    "958632c1-846a-11e5-806e-0021855f216f": "Псков Алмазная",
    "96dd9447-8fcf-11e3-aa79-0c84dcd0233a": "Смоленск Тихвинка",
    "e37a0bbb-f47f-11e4-aec3-208984863fbe": "Санкт-Петербург",
    "3445c227-7efc-11e5-be77-24fd52940c70": "Псков Шоссейная",
    "d5af83ae-68e6-11e5-8261-c48e8f4373aa": "Петрозаводск Розница",
    "ae56cf28-bd24-11e2-b408-1c6f652af6ec": "Смоленск Розница",
    "1d162cd3-886a-11e5-96e1-14dae9ee1802": "Псков Неелово",
}

with open('new-1c-data.json', 'r') as file:
    data = json.load(file)

    for cursor in data:
        related_product = product_qs.filter(UID=cursor['prod_UID'])

        # Return one object from the QuerySet
        if len(related_product) > 0:
            related_product = related_product[0]

        shop = shops.get(cursor['shop_UID'])
        print(f"{related_product} Стоимость: {int(cursor['price'])}руб. Наличие: {cursor['quantity']} {shop}")




# В.Луки Розница	647af975-60ab-11e2-8971-10bf4871e437
# Псков Алмазная	958632c1-846a-11e5-806e-0021855f216f
# Смоленск Тихвинка	96dd9447-8fcf-11e3-aa79-0c84dcd0233a
# Санкт-Петербург	e37a0bbb-f47f-11e4-aec3-208984863fbe
# Оптовый	6a4a35c3-60aa-11e2-8971-10bf4871e437
# Псков Шоссейная	3445c227-7efc-11e5-be77-24fd52940c70
# Петрозаводск Розница	d5af83ae-68e6-11e5-8261-c48e8f4373aa
# Рязань Яблочкова	9cb1dfc3-7a78-11e6-ae23-00269e8edcfe
# Смоленск Розница	ae56cf28-bd24-11e2-b408-1c6f652af6ec
# Псков Неелово	1d162cd3-886a-11e5-96e1-14dae9ee1802
        
# <QuerySet [<ProductModel: 307) Сварочные электроды Esab OK 46.00P, 2.5x350 мм, 5.3 кг>]> 2800.0 1d162cd3-886a-11e5-96e1-14dae9ee1802
# <QuerySet [<ProductModel: 307) Сварочные электроды Esab OK 46.00P, 2.5x350 мм, 5.3 кг>]> 2600.0 d5af83ae-68e6-11e5-8261-c48e8f4373aa
# <QuerySet [<ProductModel: 307) Сварочные электроды Esab OK 46.00P, 2.5x350 мм, 5.3 кг>]> 980.0 9cb1dfc3-7a78-11e6-ae23-00269e8edcfe
# <QuerySet [<ProductModel: 307) Сварочные электроды Esab OK 46.00P, 2.5x350 мм, 5.3 кг>]> 0.0 6a4a35c3-60aa-11e2-8971-10bf4871e437
# <QuerySet [<ProductModel: 307) Сварочные электроды Esab OK 46.00P, 2.5x350 мм, 5.3 кг>]> 2500.0 96dd9447-8fcf-11e3-aa79-0c84dcd0233a
# <QuerySet [<ProductModel: 307) Сварочные электроды Esab OK 46.00P, 2.5x350 мм, 5.3 кг>]> 2800.0 958632c1-846a-11e5-806e-0021855f216f
# <QuerySet [<ProductModel: 307) Сварочные электроды Esab OK 46.00P, 2.5x350 мм, 5.3 кг>]> 2500.0 ae56cf28-bd24-11e2-b408-1c6f652af6ec
# <QuerySet [<ProductModel: 307) Сварочные электроды Esab OK 46.00P, 2.5x350 мм, 5.3 кг>]> 2800.0 3445c227-7efc-11e5-be77-24fd52940c70
# <QuerySet [<ProductModel: 307) Сварочные электроды Esab OK 46.00P, 2.5x350 мм, 5.3 кг>]> 2420.0 e37a0bbb-f47f-11e4-aec3-208984863fbe
# <QuerySet [<ProductModel: 307) Сварочные электроды Esab OK 46.00P, 2.5x350 мм, 5.3 кг>]> 2725.0 647af975-60ab-11e2-8971-10bf4871e437