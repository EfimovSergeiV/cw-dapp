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

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent




# Получаем список разделов xls файла
xl = pd.ExcelFile(f'{BASE_DIR}/files/prices/PriceFubag.xlsx')
sheet_list = xl.sheet_names

print(sheet_list)


for sheet_name in sheet_list[ 0:1 ]:
    df = pd.read_excel(f'{BASE_DIR}/files/prices/PriceFubag.xlsx', sheet_name=sheet_name, header=None, index_col=0)


    # Бежим по строкам, обрабатываем колонки
    for index, row in df.iterrows():
        print(f'{row[1]}\t{row[10]}RUB\t{row[2]}')







# from elasticsearch_dsl import Search
# from elasticsearch import Elasticsearch
# client = Elasticsearch()
# s = Search(using=client)
# document_class = ProductDocument


# search_query = 'Источник для сварки под флюсом SW 1000 (38 672) + трактор сварочный TW 1000 (38 673) + набор соединительных кабелей (38847)'


# s = Search().using(client).query("match", name=search_query,)
# query = Q('match', name=search_query)
# search = document_class.search().query(query)
# response = search.execute()


# def word_list(text):
#     """ Чистит текст запроса и возвращает список слов из запроса """
#     return text.replace('(', '').replace(')', '').replace('+', '').replace('-', '').split()


# print(f'\n\nsearch query: { word_list(search_query) }\n')
# print(f'\nFound { len(response) }/{ response.hits.total.value } hit(s) for query: "{ search_query }"\n')

# word_list_query = word_list(search_query)

# for product in response:
    
#     word_list_product = word_list(product.name)
#     lenght_word_list_product = len(word_list_product)

#     like = 0

#     for word in word_list_product:
#         if word in word_list_query:
#             like += 1

#     print(f'like: { like }/{ lenght_word_list_product },  name: { word_list(product.name) }')


