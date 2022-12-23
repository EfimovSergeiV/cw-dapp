"""

Мигрирование цен товаров в единое поле

"""

from django.core.management.base import BaseCommand, CommandError
from catalog.models import *
import csv


class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


count = 0
queryset = ProductModel.objects.filter(activated=True)


for product in queryset:
    count += 1
    print(f"{ count }. id: { product.id } name: { product.category_id }")


# with open('/home/anon/docs/prods.csv', 'w', newline='') as csv_file:
    
#     fieldnames = [ 'id', 'name', ]
#     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#     writer.writeheader()
    
#     for product in queryset:
#         count += 1
#         writer.writerow({'id': f'{ product.id }', 'name': f'{ product.name }'})

#         print(f"{ count }. id: { product.id } name: { product.name } ")

