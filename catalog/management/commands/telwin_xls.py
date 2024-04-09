"""
Парсер xls файлов для Telwin загружаемый из вкладки "Товары" в личном кабинете
"""

from django.core.management.base import BaseCommand, CommandError
from catalog.models import *
from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass

qs_products = ProductModel.objects.filter(activated=True)
df = pd.read_excel(f'{BASE_DIR}/TelwinPrice.xlsx', sheet_name='Sheet1', header=None, index_col=0)

find_count = 0
actual_prices = {}
for index, row in df.iterrows():
    if row[1] not in actual_prices:
        actual_prices[row[1]] = { "name": index, "price": row[3].split(' ')[0] }
    else:
        continue

counter = 0
for qs_product in qs_products.filter(brand = 13):
    counter += 1
    print( counter, qs_product.vcode, qs_product.name, actual_prices.get(int(qs_product.vcode)))

    if actual_prices.get(int(qs_product.vcode)):
        price = actual_prices.get(int(qs_product.vcode)).get('price')
        if price != "Нет":
            qs_products.filter(id=qs_product.id).update(only_price=int(price))
            print(f"Действие: обновляем цену на { int(price) }")
        else:
            qs_products.filter(id=qs_product.id).update(only_price=None)
            print("Действие: удаляем цену")
    else:
        qs_products.filter(id=qs_product.id).update(activated=False)
        print("Действие: отключаем товар")
