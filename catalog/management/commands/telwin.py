from django.core.management.base import BaseCommand, CommandError
from catalog.models import *
import xlsxwriter
from pathlib import Path

import json
import pandas as pd
from time import sleep


from catalog.models import ProductModel


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass



def clean_word(text):
    """ Чистим название """
    return str(text).replace('*', '').replace('_', '').replace('NEW', '').lstrip().rstrip()


def beautiful_price(price):
    """ Делаем красивую стоимость, повышая до ближайшего краного 10 """
    while price % 10 != 0:
        price += 1    
    return price


path_prices = {
    'fubag' : f'{ BASE_DIR }/prices/Fubag-01-03-2023.xlsx',
    'svarog': f'{ BASE_DIR }/prices/PriceSvarog.xlsx',
    'telwin': f'{ BASE_DIR }/prices/PriceTelwin.xlsx',
}

fields_prices = {
    'fubag' : { "vcode": 1,       "name": 2, "old_name": 4,    "price": 10, "if": 0, "of": 1 },
    'svarog': { "vcode": 'index', "name": 1, "old_name": None, "price": 6,  "if": 1, "of": 2 },
    'telwin': { "vcode": 'index', "name": 1, "old_name": None, "price": 4,  "if": 0, "of": 1 },
}


prices = {}

file_path = '/home/anon/PRICES/Telwin-03-2023.xlsx'


products_qs = ProductModel.objects.filter(activated = True)


counter = 0

brand = 'telwin'

xl = pd.ExcelFile(file_path)    # read_only=True if openpyxl > 3.1.0 
sheet_list = xl.sheet_names     # print(sheet_list)        

for sheet_name in sheet_list[ fields_prices[brand]["if"] : fields_prices[brand]["of"] ]:
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, index_col=0)

    for index, row in df.iterrows():



        if type(row[fields_prices[brand]["price"]]) == int:
            vcode = clean_word(index)

            product = products_qs.filter(vcode = vcode)

            print(f"{ vcode }\t{ product}")