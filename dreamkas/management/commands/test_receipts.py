from collections import OrderedDict
from django.core.management.base import BaseCommand
import requests, json
from django.conf import settings
from payment.bridge import *

from orders.models import CustomerModel

""" Тестовая фискализация чека """


class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass

order = {'uuid': 'e68b5863-70e2-4516-92ee-c267a2fa4f27', 'order_number': 'PSK1500733', 'adress': 'Псков, ул.Леона Поземского, 92, Павильон 28 (рынок на Алмазной)', 'total': 48, 'delivery': False, 'delivery_adress': 'this.deliverycity', 'delivery_summ': 0, 'person': None, 'phone': '89116965424', 'email': 'efimovsergeiv@gmail.com', 'comment': None, 'company': None, 'legaladress': None, 'inn': None, 'kpp': None, 'okpo': None, 'bankname': None, 'currentacc': None, 'corresponding': None, 'bic': None, 'client_product': [OrderedDict([('id', 219), ('product_id', 1603), ('vcode', '816251'), ('name', 'Cварочный аппарат TECHNOLOGY 236 XT MPGE+ACX+ALU C.CASE'), ('price', '10'), ('preview_image', 'http://127.0.0.1:8000/files/img/c/preview/prodlk.jpg'), ('quantity', 2)]), OrderedDict([('id', 220), ('product_id', 718), ('vcode', 'u-718'), ('name', 'Cварочный инвертор AuroraPRO STRONGHOLD 315M'), ('price', '10'), ('preview_image', 'http://127.0.0.1:8000/files/img/c/preview/strong-315.png'), ('quantity', 2)]), OrderedDict([('id', 221), ('product_id', 719), ('vcode', 'u-719'), ('name', 'Cварочный инвертор AuroraPRO STRONGHOLD 400M'), ('price', '8'), ('preview_image', 'http://127.0.0.1:8000/files/img/c/preview/strong-400.png'), ('quantity', 1)])]}

# Генерируем данные для чека
receipts_data = generate_order(order=order)


# Фискализируем чек
check = receipting_dreamkas(data=receipts_data)
print(check)

# print(check)
