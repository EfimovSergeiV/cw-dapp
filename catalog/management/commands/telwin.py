"""

Обработка цен (пока только Telwin)

"""

from django.core.management.base import BaseCommand, CommandError
from catalog.models import *

import xlsxwriter, openpyxl, json
import pandas as pd


class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


count = 0

category = CategoryModel.objects.all()
queryset = ProductModel.objects.filter(activated=True).filter(brand=13)
prices_qs = PriceModel.objects.all()

currency = {
    "CNY": 8.82,
    "USD": 95,
    "EUR": 95,
    "RUB": 1
}



# for prod_qs in queryset:
#     print(prod_qs.name)


# df = pd.read_excel('/home/anon/PRICES//PriceTelwin.xlsx', header=None, index_col=0)
# print(df)
# # for col in df:
# #     print(col)
# for index, row in df.iterrows():
#     print(f'{index} {row[1]} {row[4]}')


xl = pd.ExcelFile('/home/anon/PRICES/PriceSvarog.xlsx')
sheet_list = xl.sheet_names  # see all sheet names
print(sheet_list)

for sheet_name in sheet_list:
    df = pd.read_excel('/home/anon/PRICES/PriceSvarog.xlsx', sheet_name=sheet_name, header=None, index_col=0)
    print(df)



# df = pd.read_excel('/home/anon/PRICES/PriceSvarog.xlsx', sheet_name="Сварочное оборудование Сварог", header=None, index_col=0)
# print(df)

# # for col in df:
# #     print(col)


# for index, row in df.iterrows():
#     print(f'{index} {row[1]} {row[6]}')
