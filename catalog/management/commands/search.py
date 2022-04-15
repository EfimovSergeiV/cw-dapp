
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


# Рабочие переменные
count = 0
unique_str = str()
qs = ProductModel.objects.all()
min_slice = 7


# Данные выводов
unique_prod_names = list()
qs_list = list()


# Читаем уникальные записи
try:
    with open("catalog/management/commands/templates.json", 'r') as file:
        data = json.load(file)
        for product in reversed(data):
            string = str(product["Name"]).lower()
            
            if string != unique_str: #Уникальные записи
                unique_str = string
                count += 1
                unique_prod_names.append(string)
                prod_name = string

                # Генерируем запросы в базу для фильтрации по базе
                for prod_name in unique_prod_names:
                    prod_name_len = len(prod_name)
                    count_name_len = len(prod_name)
                    search_count = 0
                    querysets = list()

                    try:
                        while count_name_len > min_slice:
                            # Счётчик для найденных

                            for shift in range(0, prod_name_len - count_name_len, 1):
                                search_str = prod_name[ shift : shift + count_name_len + 1 ]
                                qs_s = qs.filter(name__lower__contains=search_str)

                                if len(qs_s) in range(1, 5) :
                                    print("  /Найдено:", len(qs_s), '\t/Запрос:', search_str)
                                    for qs_success in qs_s:
                                        if qs_success not in querysets:
                                            querysets.append(qs_success)

                                else:
                                    print('\033[31m  /Найдено: %s \033[0m' %(len(qs_s)), '\033[31m /Запрос: %s \033[0m' %(search_str))

                            count_name_len -= 1
                    except:
                        continue


                    # print(product['prod_UID'])
                    print(
                        "\n\nМы искали: \t",
                        prod_name.upper(),
                        product['prod_UID'],
                        "\n", product["VendorCode"], product["price"],
                        "\n\nЕсли он есть в списке, введите его номер:\n")
                    for queryset in querysets:
                        print(search_count, queryset.name, '(id =', queryset.id, ')')
                        search_count += 1

                    select_qs = input("ВВОД: ")


                    if len(select_qs) > 0:

                        write_status = ProductModel.objects.filter(id=querysets[int(select_qs)].id).update(UID=product['prod_UID'])
                        data_str = str({querysets[int(select_qs)].id : { "name": product['Name'], "uid": product['prod_UID'] }})
                        with open('write_data.txt', 'a') as file:
                            file.write(data_str + '\n')
                        status = '!!! Данные записаны' if write_status == 1 else "!!! Произошла ошибка записи"
                        print(status)
                        time.sleep(1)

                    else:
                        with open('notfound_data.txt', 'a') as file:
                            err_prod = str({ "vcode": product["VendorCode"], "name": product["Name"], "uid": product["prod_UID"], "price": str(product["price"]) })
                            file.write(err_prod + '\n')


except KeyboardInterrupt:
    print("\nВыход из скрипта")