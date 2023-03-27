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



fields_prices = {
    'fubag' : { "vcode": 1,       "name": 2, "old_name": 4,    "price": 10, "if": 0, "of": 1 },
    'svarog': { "vcode": 'index', "name": 1, "old_name": None, "price": 6,  "if": 1, "of": 2 },
    'telwin': { "vcode": 'index', "name": 1, "old_name": None, "price": 4,  "if": 0, "of": 1 },
}


prices = {}

file_path = f'{BASE_DIR}/files/xlsx/Telwin-03-2023.xlsx'


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

            product = products_qs.filter(vcode = vcode).order_by('-id')

            print(f'\n\nSEARCH REQUEST: { vcode } { product }')

            if len(product) == 1:
                print(f"{ vcode }\t{ product[0].only_price } => { beautiful_price(row[fields_prices[brand]['price']]) }\t{ clean_word(row[fields_prices[brand]['name']]) }")
                
                id = product[0].id

                product.filter(id = id).update(
                    only_price = beautiful_price(row[fields_prices[brand]['price']]),
                    only_price_status = True,
                    name = clean_word(row[fields_prices[brand]['name']])
                )
                print(f'Rewrited: {id} {product[0]}')

            elif len(product) > 1:
                id = product[0].id
                product.filter(id = id).update(
                    only_price = beautiful_price(row[fields_prices[brand]['price']]),
                    only_price_status = True,
                    name = clean_word(row[fields_prices[brand]['name']])
                )
                ids = [ prod.id for prod in product[1:] ]
                product.filter(id__in = ids).update(
                    activated = False
                )

                print(f"{ vcode }\t{ product[0].only_price } => { beautiful_price(row[fields_prices[brand]['price']]) }\t{ clean_word(row[fields_prices[brand]['name']]) }")
                print(f'Rewrited: { id } {product[0]}')
                print(f'Dissable: { ids } { product[ 1 : ]}')
            else:
                print(f"NOT FOUND: { vcode }")
                