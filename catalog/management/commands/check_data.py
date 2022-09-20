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


qs_prods = ProductModel.objects.filter(activated=True)

for product in qs_prods:
    if len(product.description) < 40:
        print(product.id, product.name)

