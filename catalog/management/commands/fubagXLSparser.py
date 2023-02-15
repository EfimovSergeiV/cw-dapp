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


search_query = 'Источник для сварки под флюсом SW 1000 (38 672) + трактор сварочный TW 1000 (38 673) + набор соединительных кабелей (38847)'

name = 'FUBAG Источник для сварки под флюсом SW 1250'
# name = 'FUBAG сварочный трактор TW 1000'
# name = 'FUBAG источник SW 1000'
# name = 'Автомат для сварки MZ 1000'
# name = 'FUBAG сварочный трактор TW 1250'
# name = 'Электрогенератор EUROLUX G4000A 64/1/38'
# name = 'IDEALARC DC-1000'
# name = 'VERSOTRAC EWT 1000'
# name = 'Преобразователь CONVERTER 1000'
# name = 'Блок подачи воздуха PAPR 1000 mm Hose'



s = Search().using(client).query("match", name=search_query,)

query = Q('match', name=search_query)
search = document_class.search().query(query)
response = search.execute()



def word_list(text):
    """ Чистит текст запроса и возвращает список слов из запроса """
    return text.replace('(', '').replace(')', '').replace('+', '').replace('-', '').split()



print(f'\n\nsearch query: { word_list(search_query) }\n')

word_list_query = word_list(search_query)

for product in response:
    
    word_list_product = word_list(product.name)
    lenght_word_list_product = len(word_list_product)

    like = 0

    for word in word_list_product:
        if word in word_list_query:
            like += 1

    print(f'like: { like }/{ lenght_word_list_product },  name: { word_list(product.name) }')


"""
like: 6/8,  name: ['FUBAG', 'Источник', 'для', 'сварки', 'под', 'флюсом', 'SW', '1250']
like: 4/5,  name: ['FUBAG', 'сварочный', 'трактор', 'TW', '1000']
like: 2/4,  name: ['FUBAG', 'источник', 'SW', '1000']
like: 3/5,  name: ['Автомат', 'для', 'сварки', 'MZ', '1000']
like: 3/5,  name: ['FUBAG', 'сварочный', 'трактор', 'TW', '1250']
like: 0/4,  name: ['Электрогенератор', 'EUROLUX', 'G4000A', '64/1/38']
like: 0/2,  name: ['IDEALARC', 'DC1000']
like: 1/3,  name: ['VERSOTRAC', 'EWT', '1000']
like: 1/3,  name: ['Преобразователь', 'CONVERTER', '1000']
like: 1/7,  name: ['Блок', 'подачи', 'воздуха', 'PAPR', '1000', 'mm', 'Hose']
"""


print(f'\nFound { len(response) }/{ response.hits.total.value } hit(s) for query: "{ search_query }"\n')




# for word in word_list(name):
#     print(word)

# print('\n')

# for word in word_list(search_query):
#     print(word)


# print(clearing_request(search_query))



# FUBAG IQ 180

# products_qs = ProductModel.objects.filter(brand_id = 1).order_by('id')
# count = 0

# for product_qs in products_qs:
#     count += 1
#     print(f'{ count }.\t{ product_qs.only_price } RUB\t{ product_qs.name }')

