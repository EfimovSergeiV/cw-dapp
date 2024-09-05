""" 
    Rebuild OpenSearch index for all products
"""

from main.conf import OPENSEARCH_DSL
from opensearchpy import OpenSearch
from django.core.management.base import BaseCommand
from catalog.models import ProductModel, ExtendedProductModel


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        pass


opensearch_client = OpenSearch(
    hosts = [{'host': 'opensearch.glsvar.ru', 'port': 443}],
    http_auth = OPENSEARCH_DSL['default']['http_auth'],
    use_ssl = True,
    verify_certs = True
)


coordinates = {
    '1': '57.8319118,28.3073081', # Псков, ул.Леона Поземского, 92, Павильон 28 (рынок на Алмазной)
    '2': '57.8394931,28.3138475', # Псков, ул.Шоссейная д.3а
    '3': '57.7936692,28.2092483', # Псков, пос. Неёлово,
    '4': '56.3389457,30.5331372', # Великие Луки, проспект Ленина д.57  
    '5': '54.7425144,32.0828188', # Смоленск, ул. Посёлок Тихвинка 69, ТК "Город Мастеров" павильон №73
    '6': '61.8161181,34.3078504', # Петрозаводск, ул. Заводская, д. 2
}





def index_document(index_name, doc_id, document):
    response = opensearch_client.index(
        index=index_name,
        id=doc_id,
        body=document,
        refresh=True 
    )
    return response



for product in ProductModel.objects.filter(activated=True):
    index_name = 'products'
    document = {
        'id': product.id,
        'vcode': product.vcode,
        'name': product.name,
        'keywords': product.keywords,
    }
    response = index_document(index_name, doc_id=product.id, document=document)


    print(f'{ document["id"]}\t{response["result"]} {response["_index"]} {document["name"]}')



for product in ExtendedProductModel.objects.all():
    index_name = 'ext_products'
    document = {
        'id':   product.id,
        'name': product.name,
        'city': product.city,
        'shop': product.shop,
        'geo_point': coordinates[str(product.shop_id)],
        'price': product.price,
        'quantity': product.quantity,
    }

    response = index_document(index_name, doc_id=product.id, document=document)


    print(f'{ document["id"]}\t{response["result"]} {response["_index"]} {document["city"]} {document["name"]}')



