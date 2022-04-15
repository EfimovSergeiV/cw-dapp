from django.core.management.base import BaseCommand
from catalog.models import *
import json


class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


qs_prop = PropStrModel.objects.all()

# for ['7z26', 'ilav']


with open("prods.json", 'w') as file:
    for prop in qs_prop:
        if prop.qname in ['7z26', 'ilav', '2rzq', 'wvf1']:

            a = f" ВЕС: { str(prop.value) } \t { str(prop.product) } \n"   #'Вес:', str(prop.value) + '  ' +  str(prop.product)
            file.write(a)