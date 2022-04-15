from django.core.management.base import BaseCommand, CommandError
from django.db.models.functions.text import Left, Length
from rest_framework import serializers
from catalog.models import *
import os
import json
from django.db.models.functions import Lower
from django.db.models import CharField
import time

CharField.register_lookup(Lower)





class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass

qs = ProductModel.objects.all() 


def reise_search(string, min_slice=6):
    """
    Срезает строку по одному символу и сдвигает вправо срез, для поиска
    print(count, string, '\033[31m <%s> \033[0m' %(lenght))
    """

    qs = ProductModel.objects.all()

    print("Количество записей (qs): ", len(qs))


    unfilter_qs = []

    ########################
    length_str = len(string)
    now_lenght = len(string)


    while now_lenght > min_slice:


        max_range_int = length_str - now_lenght
        for shift in range(0, max_range_int + 1, 1):
            wort_slice = string[ shift : shift + now_lenght ].lower()

            sear = str(wort_slice)


            qs_s = qs.filter(name__lower__contains=sear)

            if len(qs_s) > 0 :
                print("/Найдено: ", len(qs_s), '/Запрос: ', sear) # Строка для запроса
            else:
                print('\033[31m  /Найдено: %s \033[0m' %(len(qs_s)), '\033[31m /Запрос: %s \033[0m' %(sear),) # Строка для запроса


            if len(qs_s) in range(1, 5):
                unfilter_qs.append(qs_s)



        now_lenght -= 1
        ###############


    return unfilter_qs


# qs = qs.filter(name__lower__contains="ство overman 250/aur")
# print(len(qs))

querysets = list()
unique_str = str()
count = int()
logs = list()


# try: # На остановку пользователем
#     with open("/home/anon/dev/glsvar-dapp/catalog/management/commands/templates.json", 'r') as file:
#         data = json.load(file)
#         for product in data:
#             string = product["Name"] #.lower()
            
#             if string != unique_str: #Уникальные записи
#                 unique_str = string
#                 count += 1
                

#                 # print(count, product["prod_UID"], string, product["VendorCode"])
#                 text = str(count) + ' ' + product["prod_UID"] + ' ' + string + ' ' + str(product["VendorCode"])

#                 qset = reise_search(string=string)
#                 # print(qset)

#                 # wait_ex = input("(y/N) Продолжаем ? >>> ")

#                 # if wait_ex == 'n' or 'N':
#                 #     break



#                 # print(text)

#                 # logs.append(str(text))


#     # with open('test.txt', 'w') as file:
#     #     for line in logs:
#     #         file.write(line + '\n')

    
    

# except KeyboardInterrupt:
#     print("STOP PARSING")
#     print(len(querysets))

for string in [
    'Инвертор сварочный TIG 180 DSP "PRO',
    'Сварочный полуавтомат SPEEDWAY 175 Aurora-Pro',
    'Сварочный полуавтомат  INMIG 315 T в комплекте'
]:

    result = reise_search(string=string)
    print(result)


