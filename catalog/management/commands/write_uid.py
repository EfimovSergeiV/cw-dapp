from django.core.management.base import BaseCommand, CommandError
from django.db.models.functions.text import Left, Length
from django.db.models.query_utils import Q
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


qs_prod = ProductModel.objects.all()



with open('catalog/management/commands/unparse.json') as file:
    data = json.load(file)
    for product in data:
        # print(product['id'])

        status = qs_prod.filter(id=product['id']).update(UID=product['uid'])
        print(status, product['name'])