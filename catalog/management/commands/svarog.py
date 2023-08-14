"""

1. СВАРОГ - ПОВЫШЕНИЕ ЦЕН НА X%

"""

from django.core.management.base import BaseCommand, CommandError
from catalog.models import *
import csv, requests, json
import xlsxwriter
import math


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        pass


PROCENT = 10

count = 0
queryset = ProductModel.objects.filter(activated=True)

for prod_qs in queryset.filter(brand=9).order_by('id'):
    count += 1
    new_price = int((prod_qs.only_price / 100) * PROCENT + prod_qs.only_price)

    price = new_price

    while price % 10 != 0:
        price += 1

    print(f'{count}. { prod_qs.id }: { prod_qs.only_price } > { price } { prod_qs.name }')

    queryset.filter(id=prod_qs.id).update(only_price = price)