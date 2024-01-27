from django.core.management.base import BaseCommand, CommandError
from catalog.models import *
import xlsxwriter
from pathlib import Path

import json
import pandas as pd
from time import sleep


from content.models import ReviewsModel


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


# props = PropStrModel.objects.all()
props = PropStrModel.objects.all()



# for prop in props:

#     if ',' in prop.value or prop.qvalue:

#         qvalue = prop.qvalue if prop.qvalue is None else prop.qvalue.replace(",", ".")
#         print(f'{ prop.name } - { prop.value.replace(",", ".") } \ { prop.qname } - { qvalue }')



# for

# from orders.models import *


# qs = RequestPriceModel.objects.all()

# print('hallo')
# for client in qs:
#     if '@' in client.contact:
#         print(client.contact)

arr_clients = []

with open('clients.txt', 'r') as file:
    clients = file.readlines()

    for client in clients:
        if client not in arr_clients:
            arr_clients.append(client)
            print(client)


with open('clear_client.txt', 'w') as file:
    for cl in arr_clients:
    
        file.write(cl)
