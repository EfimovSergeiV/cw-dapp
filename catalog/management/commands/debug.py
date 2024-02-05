from django.core.management.base import BaseCommand, CommandError
from catalog.models import *
import xlsxwriter, requests
from pathlib import Path

import json
import pandas as pd
from time import sleep


from content.models import ReviewsModel


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


# props = PropStrModel.objects.all()
# props = PropStrModel.objects.all()



# for prop in props:

#     if ',' in prop.value or prop.qvalue:

#         qvalue = prop.qvalue if prop.qvalue is None else prop.qvalue.replace(",", ".")
#         print(f'{ prop.name } - { prop.value.replace(",", ".") } \ { prop.qname } - { qvalue }')



# for

# from orders.models import *


# qs = RequestPriceModel.objects.all()

# print('hallo')
# for client in qs:
#     if '@' in client.contact:
#         print(client.contact)

# arr_clients = []

# with open('clients.txt', 'r') as file:
#     clients = file.readlines()

#     for client in clients:
#         if client not in arr_clients:
#             arr_clients.append(client)
#             print(client)


# with open('clear_client.txt', 'w') as file:
#     for cl in arr_clients:
    
#         file.write(cl)




url = "http://127.0.0.1:8000/o/order/"
data = {'shop_id': 1, 'region_code': 'SPE', 'person': 'Иван Иванов', 'phone': '+79116965424', 'email': None, 'comment': 'Тестовый заказ', 'delivery': False, 'adress': 'Санкт-Петербург, шоссе Революции, д.84, литера Е', 'total': 16700, 'promocode': None, 'company': None, 'legaladress': None, 'inn': None, 'kpp': None, 'okpo': None, 'bankname': None, 'currentacc': None, 'corresponding': None, 'bic': None, 'client_product': [{'id': 1694, 'vcode': '51MS705', 'name': 'Маска сварщика хамелеон АСФ 705', 'rating': '5.0', 'only_price': 4500, 'status': 'stock', 'preview_image': 'http://127.0.0.1:8000/files/img/c/preview/3.webp', 'propstrmodel': [{'id': 9959, 'name': 'Размер, см', 'qname': None, 'value': '52-65'}, {'id': 9960, 'name': 'Сроки хранения, мес', 'qname': None, 'value': '60'}, {'id': 9961, 'name': 'Срок эксплуатации, мес', 'qname': None, 'value': '12'}, {'id': 9962, 'name': 'Страна изготовитель', 'qname': None, 'value': 'Россия'}, {'id': 9975, 'name': 'Оптический класс светофильтра', 'qname': None, 'value': '1/1/1/2'}, {'id': 9976, 'name': 'Поле зрения, мм', 'qname': None, 'value': '100х53'}, {'id': 9977, 'name': 'Затемнение в светлом состоянии', 'qname': None, 'value': 'DIN 4'}, {'id': 9978, 'name': 'Регулировка степени затемнения', 'qname': None, 'value': 'Плавная'}, {'id': 9979, 'name': 'Регулятор затемнения', 'qname': None, 'value': 'Наружный'}, {'id': 9980, 'name': 'Включение/ Выключение', 'qname': None, 'value': 'Автоматическое'}, {'id': 9981, 'name': 'Регулятор чувствительности', 'qname': None, 'value': 'Плавная регулировка'}, {'id': 9982, 'name': 'Защита от УФ/Ик излучения', 'qname': None, 'value': 'До13 DIN'}, {'id': 9983, 'name': 'Источник питания', 'qname': None, 'value': 'Солнечная батарея сменный элемент питания'}, {'id': 9984, 'name': 'Время срабатывания, сек', 'qname': None, 'value': '1/30000'}, {'id': 9985, 'name': 'Время задержки, сек', 'qname': None, 'value': 'Плавная 0,1-1,0'}, {'id': 9986, 'name': 'Режим шлифовки', 'qname': None, 'value': 'Есть'}, {'id': 9987, 'name': 'Температура эксплуатации, С', 'qname': None, 'value': 'ОТ -5 ДО +55'}, {'id': 9988, 'name': 'Материал маски', 'qname': None, 'value': 'Ударопрочный пластик'}], 'quantity': 1}, {'id': 1695, 'vcode': '51ST201D', 'name': 'Маска сварщика BASIC', 'rating': '5.0', 'only_price': 400, 'status': 'stock', 'preview_image': 'http://127.0.0.1:8000/files/img/c/preview/5_1.webp', 'propstrmodel': [{'id': 9963, 'name': 'Размер, см', 'qname': None, 'value': '52-65'}, {'id': 9964, 'name': 'Срок хранения, мес', 'qname': None, 'value': '60'}, {'id': 9965, 'name': 'Срок эксплуатации, мес', 'qname': None, 'value': '12'}, {'id': 9966, 'name': 'Страна изготовитель', 'qname': None, 'value': 'Россия'}], 'quantity': 3}, {'id': 817, 'vcode': '991900', 'name': 'Сварочная маска FUBAG BLITZ 9-13 Visor', 'rating': '4.9', 'only_price': 11000, 'status': 'order', 'preview_image': 'http://127.0.0.1:8000/files/img/c/preview/prodd_9DddxhK.webp', 'propstrmodel': [{'id': 4639, 'name': 'Количество сенсоров', 'qname': '65gg', 'value': '4'}, {'id': 4641, 'name': 'Размер экрана, мм', 'qname': '8xs2', 'value': '97 х 62'}, {'id': 4643, 'name': 'Питание', 'qname': 'b58b', 'value': 'солн. эл. + 2 бат.'}, {'id': 4644, 'name': 'Масса, кг', 'qname': 'czsb', 'value': '0.48'}, {'id': 4640, 'name': 'Регулировка степени затемнения', 'qname': 'ewcy', 'value': 'внутренняя'}, {'id': 4637, 'name': 'Диапазон светопропускания, DIN', 'qname': 'f8yu', 'value': '9-13'}, {'id': 4633, 'name': 'Регулировка чувствительности', 'qname': 'm847', 'value': 'да'}, {'id': 4638, 'name': 'Защита от УФ/ИК-излучения, DIN', 'qname': 'q4z6', 'value': '16'}, {'id': 4642, 'name': 'Вкл/Выкл питания', 'qname': 'q9r4', 'value': 'автомат'}, {'id': 4636, 'name': 'Время переключения в тёмное состояние, сек', 'qname': 'rrax', 'value': '1/25000'}, {'id': 4635, 'name': 'Время переключения в светлое состояние, сек', 'qname': 'wdp9', 'value': '0,10 - 1,00'}, {'id': 4634, 'name': 'Световой режим, DIN', 'qname': 'z70n', 'value': '3,5'}], 'quantity': 1}]}


resp = requests.post(url=url, data=data)
print(resp.status_code)