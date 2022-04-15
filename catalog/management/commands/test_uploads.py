from django.core.management.base import BaseCommand, CommandError
from django.db.models.functions.text import Left, Length
from rest_framework import serializers
from catalog.models import *
import os
import json
from django.db.models.functions import Lower
from django.db.models import CharField
import time
import datetime


CharField.register_lookup(Lower)


class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass

date_name = datetime.datetime.now().date()
filename =  'uploads/' + str(date_name) + '.json'


try:
    with open(filename, 'r') as file:
        data = json.load(file)
        while True:
            uid = input("\nENTER PRODUCT UID: ")
            for product in reversed(data):
                if product['prod_UID'] == uid:
                    print(
                        product['prod_UID'], 
                        product['shop_UID'],
                        product['price'], 
                        product['currency'], 
                    )
                else:
                    pass
            if uid in ('q', 'exit', 'stop'):
                print("\nCLOSE WORK TEST")
                break

except KeyboardInterrupt:
    print("\nCLOSE WORK TEST")

except:
    print("\nFIRST ERR")