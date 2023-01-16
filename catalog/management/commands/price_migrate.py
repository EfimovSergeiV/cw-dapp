"""



1. Экспорт цен в таблицу с разбором стоимости валюты и общей цены

"""

from django.core.management.base import BaseCommand, CommandError
from catalog.models import *
import csv, requests, json
import xlsxwriter


class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


count = 0

category = CategoryModel.objects.all()
queryset = ProductModel.objects.filter(activated=True)
prices_qs = PriceModel.objects.all()

currency = {
    "CNY": 8.82,
    "USD": 95,
    "EUR": 95,
    "RUB": 1
}

expenses = []

for qs_ct in category:
    # print(f'{ qs_ct.id } { qs_ct.name }')
    expenses.append([qs_ct.id, qs_ct.name, 'category',])

    for product in queryset.filter(category=qs_ct.id):
        """ + Добавить к парсеру наличие товаров """
        
        count += 1

        if product.only_price_status:
            price = int(product.only_price * currency[product.currency])
            print(f"\n{ count }\nid: { product.id }\nname: { product.name }\nO: { price } TRUE")

            product = [product.id, product.name, price]
        else:
            price_qs = prices_qs.filter(product = product.id)
            price = int(price_qs[0].price * currency[price_qs[0].currency])
            print(f"\n{ count }\nid: { product.id }\nname: { product.name }\nO: {price}")

            product = [product.id, product.name, price]




        expenses.append(product)























# workbook = xlsxwriter.Workbook('/home/anon/backup/prods.xlsx')   # Сменить путь для сервера
# worksheet = workbook.add_worksheet()

# bold = workbook.add_format({'bold': True})
# name = workbook.add_format()

# worksheet.set_column(0, 0, 10)
# worksheet.set_column(1, 1, 120)
# worksheet.set_column(2, 2, 10)

# worksheet.write('A1', 'id', bold)
# worksheet.write('B1', 'Название', bold)
# worksheet.write('C1', 'Стоимость', bold)

# row = 1
# col = 0

# for id, name, price in (expenses):
#     if price == 'category':
#         row += 2

#         worksheet.write(f'A{row}', id, bold)
#         worksheet.write(f'B{row}', name, bold)

#     else:
#         worksheet.write(row, col, id, )
#         worksheet.write(row, col + 1, name)
#         worksheet.write(row, col + 2, price)
#     row += 1

# workbook.close()
