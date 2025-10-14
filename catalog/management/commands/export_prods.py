from django.core.management.base import BaseCommand, CommandError
from catalog.models import *
import xlsxwriter, requests
from pathlib import Path

import json
from user.models import UserWatcherModel
from time import sleep


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass

print("hallo welt")

products = {}

# Получаем категории первого уровня
for cat in CategoryModel.objects.filter(parent=None, activated=True):
    print(f"{cat.id} {cat.name}")

    products[f"{cat.name}"] = []

    # Получаем продукты в категории с учетом подкатегорий
    prods = ProductModel.objects.filter(category__in=CategoryModel.objects.filter(parent=cat, activated=True), activated=True).distinct()
    for prod in prods:
        
        try:
            id, brand, name = prod.id, prod.brand.brand, prod.name
        except:
            id, brand, name = prod.id, "Не указан", prod.name

        price = prod.only_price if prod.only_price else "Цена не указана"

        print(f"{id} {brand} {name} {price}")

        products[f"{cat.name}"].append({
            "id": id,
            "brand": brand,
            "name": name,
            "price": price
        })

print(products)

# Создаем новый Excel, создавая отдельные таблицы для каждой категории
workbook = xlsxwriter.Workbook(f"{BASE_DIR}/products.xlsx")
cell_format = workbook.add_format({'align': 'left'})
for cat_name, prods in products.items():
    worksheet = workbook.add_worksheet(cat_name)
    # ширина столбцов: B = 5см, C = 18, D = 5см
    worksheet.set_column(1, 1, 14.2)  # B, 5см
    worksheet.set_column(2, 2, 61.2)  # C, 18см
    worksheet.set_column(3, 3, 18.2)  # D, 5см
    worksheet.write(0, 0, "id", cell_format)
    worksheet.write(0, 1, "Бренд", cell_format)
    worksheet.write(0, 2, "Название", cell_format)
    worksheet.write(0, 3, "Цена", cell_format)

    for row_num, prod in enumerate(prods, start=1):
        worksheet.write(row_num, 0, prod["id"], cell_format)
        worksheet.write(row_num, 1, prod["brand"], cell_format)
        worksheet.write(row_num, 2, prod["name"], cell_format)
        worksheet.write(row_num, 3, prod["price"], cell_format)

workbook.close()
print("Экспорт завершен. Файл сохранен как products.xlsx")