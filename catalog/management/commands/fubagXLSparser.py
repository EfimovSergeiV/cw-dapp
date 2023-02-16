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

from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch
client = Elasticsearch()
s = Search(using=client)
document_class = ProductDocument


def word_list(text):
    """ Чистит текст запроса и возвращает список слов из запроса """
    return text.replace('(', '').replace(')', '').replace('+', '').replace('-', '').replace('.', '').replace('_', '').split()




show_counter = 0    # Откуда начинаем спрашивать
show_value = 80


# Получаем список разделов xls файла
xl = pd.ExcelFile(f'{BASE_DIR}/files/prices/PriceFubag.xlsx')
sheet_list = xl.sheet_names


for sheet_name in sheet_list[ 0:1 ]:
    df = pd.read_excel(f'{BASE_DIR}/files/prices/PriceFubag.xlsx', sheet_name=sheet_name, header=None, index_col=0)


    # Бежим по строкам, обрабатываем колонки
    for index, row in df.iterrows():
        # print(f'{row[1]}\t{row[10]}RUB\t{row[2]}')
        
        show_counter += 1

        if type(row[2]) == str:
            search_query = row[2]

            found = { "like": 0, "name": None }
            variants = []

            s = Search().using(client).query("match", name=search_query,)
            query = Q('match', name=search_query)
            search = document_class.search().query(query)
            response = search.execute()

            # print(f'\n\nsearch query: { word_list(search_query) }\n')
            # print(f'\nFound { len(response) }/{ response.hits.total.value } hit(s) for query: "{ search_query }"\n')

            word_list_query = word_list(search_query)

            for product in response:
                
                word_list_product = word_list(product.name)
                lenght_word_list_product = len(word_list_product)

                like = 0

                # Подсчёт лайков
                for word in word_list_product:
                    if word in word_list_query:
                        like += 1

                # Создаём возможные варианты на основе ответа Еластика
                # print(f'like: { like }/{ lenght_word_list_product },  name: { word_list(product.name) }')
                if lenght_word_list_product - like >= 4:
                    variants.append({ "like": f'{ like }/{ lenght_word_list_product }', "name": product.name })



                # Ставим лайки, тем у кого больше совпало
                if lenght_word_list_product - like > 2 and like > found['like']:
                    found = { "like": like, "name": product.name }


            print(f'\n\tЗапрос:\t{ search_query }\n\tНашли:\t{ found["name"] }\n')

            var_count = 0
            for variant in variants:
                var_count += 1
                print(f'\t{ var_count }\t{variant["like"]}\t{variant["name"]}')


            if found['name'] and show_counter > show_value:
                action = input("\n\tПравильно? Y - yes, N - no, C - create without desk-on\n\tNumber - manual select \n\t> ")

                if action == 'y' or action ==  'Y':
                    print('\tSaving...\n\n')
                if action == 'c' or action ==  'C':
                    name = input("\tКак назовём?: ")
                    print(f'\tCreate: { name } ...\n\n')
                if action == 'e' or action ==  'E':
                    print('\tExit...\n\n')
                    break
                if action in [ str(i) for i in range(0, 10)]:
                    print(f'\tSaving: {variants[ int(action) - 1 ]["name"]} ...\n\n')

            print('\n\n\n')