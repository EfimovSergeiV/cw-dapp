from django.core.management.base import BaseCommand, CommandError
from catalog.models import *
import csv, requests, json
import xlsxwriter
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


count = 0

cts_qs = CategoryModel.objects.all()
prods_qs = ProductModel.objects.filter(activated=True)
prices_qs = PriceModel.objects.all()

status_translator = {
    "stock": "В наличии",
    "order": "Под заказ",
}


print(f'{BASE_DIR}/files/')
expenses = []

for category in [4, 14, 35, 34, 31, 28, 25 , 18, 32, 29, 23, 33, 30, 27]:
    ct_qs = cts_qs.get(id=category)

    print(f'\n{ct_qs.id} {ct_qs.name}')
    
    for ct_prods_qs in prods_qs.filter(category=category):
        status = status_translator[ct_prods_qs.status]

        product = [
            ct_prods_qs.id, 
            ct_prods_qs.name, 
            ct_prods_qs.only_price
        ]

        expenses.append(product)
        print(f'{ ct_prods_qs.id }.\t{ ct_prods_qs.only_price } RUB\t{ status }\t{ ct_prods_qs.name }')


workbook = xlsxwriter.Workbook(f'{BASE_DIR}/files/xlsx/prods-ct-4.xlsx')
worksheet = workbook.add_worksheet()

bold = workbook.add_format({'bold': True})
name = workbook.add_format()

worksheet.set_column(0, 0, 10)
worksheet.set_column(1, 1, 120)
worksheet.set_column(2, 2, 10)

worksheet.write('A1', 'id', bold)
worksheet.write('B1', 'Название', bold)
worksheet.write('C1', 'Стоимость', bold)

row = 1
col = 0

for id, name, price in (expenses):
    if price == 'category':
        row += 2

        worksheet.write(f'A{row}', id, bold)
        worksheet.write(f'B{row}', name, bold)

    else:
        worksheet.write(row, col, id, )
        worksheet.write(row, col + 1, name)
        worksheet.write(row, col + 2, price)
    row += 1

workbook.close()
