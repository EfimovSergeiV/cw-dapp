"""
Генератор sitemap
"""

from django.core.management.base import BaseCommand
from catalog.models import *



class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


queryset = ProductModel.objects.filter(activated=True)

list_id = 0
count = 0
prod_lists = []
prod_ids = []


for qs_prod in queryset:
    count += 1
    prod_ids.append(qs_prod.id)
    if count % 200 == 0:
        prod_lists.append(prod_ids)
        prod_ids = []


for ids in prod_lists:
    list_id += 1
    with open(f'list-{ list_id }.xml', 'w') as file:
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        file.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

        for id in ids:
            file.write('  <url>\n')
            file.write(f'    <loc>https://glsvar.ru/product/{ id }</loc>\n')
            file.write('  </url>\n')
            print(f'<loc>https://glsvar.ru/product/{ id }</loc>\n',)

        file.write('</urlset>\n')


print(count)
