"""
    Парвер цен Сварог

"""

from django.core.management.base import BaseCommand, CommandError
from catalog.models import *

from pathlib import Path
import xlsxwriter, openpyxl, json
import pandas as pd


class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
count = 0

category = CategoryModel.objects.all()
queryset = ProductModel.objects.filter(activated=True).filter(brand=13)
prices_qs = PriceModel.objects.all()

print(BASE_DIR)

# for prod_qs in queryset:
#     print(prod_qs.name)


# df = pd.read_excel('/home/anon/PRICES//PriceTelwin.xlsx', header=None, index_col=0)
# print(df)
# # for col in df:
# #     print(col)
# for index, row in df.iterrows():
#     print(f'{index} {row[1]} {row[4]}')



# Получаем список разделов xls файла
xl = pd.ExcelFile(f'{BASE_DIR}/files/prices/PriceSvarog.xlsx')
sheet_list = xl.sheet_names  # see all sheet names

# Бежим по разделу
for sheet_name in sheet_list[1:2]:
    df = pd.read_excel('/home/anon/PRICES/PriceSvarog.xlsx', sheet_name=sheet_name, header=None, index_col=0)
    print(df)






# df = pd.read_excel('/home/anon/PRICES/PriceSvarog.xlsx', sheet_name="Сварочное оборудование Сварог", header=None, index_col=0)
# print(df)

# # for col in df:
# #     print(col)


# for index, row in df.iterrows():
#     print(f'{index} {row[1]} {row[6]}')
