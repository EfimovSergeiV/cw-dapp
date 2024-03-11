from django.core.management.base import BaseCommand, CommandError
from catalog.models import ProductModel

import json

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


shops_uids = {
    "d5af83ae-68e6-11e5-8261-c48e8f4373aa": "Петрозаводск Розница",
    "647af975-60ab-11e2-8971-10bf4871e437": "В.Луки Розница",
    "958632c1-846a-11e5-806e-0021855f216f": "Псков Алмазная",
    "96dd9447-8fcf-11e3-aa79-0c84dcd0233a": "Смоленск Тихвинка",
    "e37a0bbb-f47f-11e4-aec3-208984863fbe": "Санкт-Петербург",
    "3445c227-7efc-11e5-be77-24fd52940c70": "Псков Шоссейная",
    "d5af83ae-68e6-11e5-8261-c48e8f4373aa": "Петрозаводск Розница",
    "ae56cf28-bd24-11e2-b408-1c6f652af6ec": "Смоленск Розница",
    "1d162cd3-886a-11e5-96e1-14dae9ee1802": "Псков Неелово",
    "9cb1dfc3-7a78-11e6-ae23-00269e8edcfe": "Москва",
}

counter = 0
with open('files/new-1c-data.json', 'r') as file:
    data = json.load(file)
    for row in data:
        if row['shop_UID'] == "9cb1dfc3-7a78-11e6-ae23-00269e8edcfe" and int(row['price']) > 20000:
            counter += 1
            print(f"{counter}.\tтовар: {int(row['price'])} руб.\tв наличии: {row['quantity']} ")

