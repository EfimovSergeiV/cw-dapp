from django.core.management.base import BaseCommand
from catalog.models import *
import json


class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


qs_prod = ProductModel.objects.all()


prod_dict = list()
    

# Write prods to file
with open("all_prod.json", 'a') as file:
    for prod in qs_prod:
        if not prod.UID:
            print(prod.id, prod.name,)
            product = "( id: " +  str(prod.id) + ") " + "Товар: " + str(prod.name)
            file.write(product + "\n")
                
