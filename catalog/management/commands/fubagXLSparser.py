from django.core.management.base import BaseCommand, CommandError
from catalog.models import *

from elasticsearch_dsl import Q
from catalog.documents import ProductDocument   #, ProductKeywordDocument

from pathlib import Path
import xlsxwriter, openpyxl, json
import pandas as pd


class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass

"""
class SearchView(APIView):
    serializer_class = SearchSerializer
    document_class = ProductDocument

    def post(self, request):
        search_query = request.data['name']
        query = Q('multi_match', query=search_query,
                fields=[
                    'vcode',
                    'name',
                    'keywords',
                ], fuzziness='auto')

        search = self.document_class.search().query(query)[0:30]
        response = search.execute()


        # Костыль для отключённых товаров
        prods = []
        for prod in response:
            prods.append(prod.id)
        qs = ProductModel.objects.filter(activated=True).filter(id__in=prods)



        # print(f'Found { len(response) }/{ response.hits.total.value } hit(s) for query: "{ search_query }"')

        serializer = self.serializer_class(qs, many=True, context={'request':request})
        return Response(serializer.data)
"""

from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch

client = Elasticsearch()

s = Search(using=client)

document_class = ProductDocument


search_query = 'Источник для сварки под флюсом SW 1000 (38 672) + трактор сварочный TW 1000 (38 673) '

s = Search().using(client).query("match", name=search_query,)

query = Q('multi_match', query=search_query,
        fields=[
            'vcode',
            'name',
            'keywords',
        ], fuzziness='auto')

search = document_class.search().query(query)
response = search.execute()


print(f'\nFound { len(response) }/{ response.hits.total.value } hit(s) for query: "{ search_query }"\n')

for product in  response:
    print(product.name)



# FUBAG IQ 180

# products_qs = ProductModel.objects.filter(brand_id = 1).order_by('id')
# count = 0

# for product_qs in products_qs:
#     count += 1
#     print(f'{ count }.\t{ product_qs.only_price } RUB\t{ product_qs.name }')

