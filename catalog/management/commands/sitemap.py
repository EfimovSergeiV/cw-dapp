""" Топорная реализация генератора sitemap.xml """

from django.core.management.base import BaseCommand
from pathlib import Path
import json

from datetime import date
from catalog.models import ProductModel


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        pass


frequency = 50
list_counter = 0
page_id = 0
list_ids = []
today = date.today()

qs_prods = ProductModel.objects.filter(activated=True)




def create_file(list_ids, page_id):
    # Генерируем файлик с товарами
    start_str = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    body = ''
    end_str = '\n</urlset>'

    for prod_id in list_ids:
        body += f"""\n  <url>
    <loc>https://glsvar.ru/product/{ prod_id }</loc>
  </url>"""

    txt = start_str + body + end_str
    with open(f'sitemap/list-{ page_id }.xml', 'w' ) as file:
        file.write(txt)




start_str = '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
body = ''
end_str = '\n</sitemapindex>'

for qs_prod in qs_prods:
    list_counter += 1

    if list_counter < frequency:
        list_ids.append(qs_prod.id)

    else:
        page_id += 1
        
        body += f"""\n  <sitemap>
    <loc>https://glsvar.ru/prods/list-{ page_id }.xml</loc>
    <lastmod>{ today }</lastmod>
  </sitemap>"""
        
        create_file(list_ids, page_id)

        list_ids, list_counter = [], 0


txt = start_str + body + end_str
with open(f'sitemap/sitemap.xml', 'w' ) as file:
    file.write(txt)

