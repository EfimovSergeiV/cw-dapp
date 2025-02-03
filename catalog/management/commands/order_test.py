from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
import json, requests



BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass






json_data = {'region_code': 'PSK', 'person': None, 'phone': 'WhatsApp 71231231212', 'email': None, 'comment': None, 'delivery': True, 'delivery_adress': 'Дедовичи', 'promocode': None, 'adress': 'Псков, пос Неёлово, ул.Юбилейная д. 5ж', 'client_product': [{'id': 40, 'vcode': 'u-40', 'description': 'Применение: ЦИНК 400 - предназначен для холодной гальванизации любых металлических материалов. Спрей (распылитель) с высоким содержанием цинка особенно хорошо подходит для закрашивания паяных и сварных соединений, восстановления или гальванизации металлических листов, гальванизации и длительной защиты болтовых соединений, эксплуатируемых в атмосферных условиях, для восстановления цинкового покрытия на воротах, дверях, металлических листах, резервуарах, металлических конструкциях. Аэрозольный баллончик снабжен защитным наконечником, препятствующим образованию капель, что позволяет получать покрытие не требующее дополнительной подкраски. ЦИНК 400 хорошо защищает от атмосферной коррозии, устойчив к воздействию соли и высокой влажности.', 'name': 'Спрей Цинк 400. Холодный цинк', 'preview_image': 'http://127.0.0.1:8000/files/img/c/preview/1_CYip9XR.webp', 'rating': '4.5', 'promo': False, 'discount': None, 'related': [106], 'ozon': 'https://ozon.ru/product/1725071148', 'only_price_status': True, 'only_price': 680, 'opt_price': 680, 'opt_quantity': 25, 'currency': 'RUB', 'status': 'stock', 'propstrmodel': [{'id': 166, 'name': 'Объём, мл', 'qname': 'cvaf', 'value': '400'}], 'category': 'Химия для сварки', 'brand': {'id': 4, 'brand': 'M-WELD', 'image': 'http://127.0.0.1:8000/files/img/c/brand/m-weld.webp', 'carousel': True, 'description': ''}, 'keywords': 'm-weld, м-велд', 'product_set': [], 'product_comp': [], 'prod_img': [{'id': 49, 'image': 'http://127.0.0.1:8000/files/img/c/prod/1_BECrAZ6.jpg'}], 'prod_doc': [], 'prod_link': [], 'opt': True, 'quantity': 75}, {'id': 114, 'vcode': 'u-114', 'description': 'Антипригарная паста предназначена для защиты сопла и наконечника\r\nгорелки от налипания брызг и образования корок, что гарантирует\r\nболее длительную службу сварочных горелок.\r\n\r\nАнтипригарная паста экологически безопасна, не токсична, не\r\nвоспламеняется, без силикона.\r\n\r\nСпособ применения:\r\nОкунуть теплую горелку в пасту на несколько секунд, извлечь и\r\nподержать некоторое время над банкой, чтобы излишняя часть пасты\r\nстекла обратно в емкость во избежание закупорки газового\r\nдиффузора.\r\n\r\nСделано в Италии специально для ООО «Техносвар КС»', 'name': 'Антипригарная Паста M-Weld', 'preview_image': 'http://127.0.0.1:8000/files/img/c/preview/1329296768.webp', 'rating': '4.7', 'promo': False, 'discount': None, 'related': [106], 'ozon': 'https://ozon.ru/product/1725123490', 'only_price_status': True, 'only_price': 600, 'opt_price': 600, 'opt_quantity': 12, 'currency': 'RUB', 'status': 'stock', 'propstrmodel': [{'id': 631, 'name': 'Объём, мл', 'qname': 'cvaf', 'value': '375'}], 'category': 'Химия для сварки', 'brand': {'id': 4, 'brand': 'M-WELD', 'image': 'http://127.0.0.1:8000/files/img/c/brand/m-weld.webp', 'carousel': True, 'description': ''}, 'keywords': 'm-weld, м-велд', 'product_set': [], 'product_comp': [], 'prod_img': [{'id': 204, 'image': 'http://127.0.0.1:8000/files/img/c/prod/1329296768.jpg'}], 'prod_doc': [], 'prod_link': [], 'opt': True, 'quantity': 48}, {'id': 1835, 'vcode': 'u-1835', 'name': 'Травильная паста M-WELD', 'description': 'Паста для травления и пассивации нержавеющей стали. Удаляет следы побежалости, ржавчину, восстанавливает свойства нержавеющей стали. Паста применяется для обработки сварных швов, мест термического взаимодействия (плазменная резка, горячая штамповка и тд), мест механического воздействия (шлифовка, резка, пескоструйная обработка и тд). После обработки пастой сварной шов и околошовная приобретает ровный матовый цвет и коррозионную стойкость нержавеющей стали.', 'promo': False, 'discount': None, 'rating': '5.0', 'preview_image': 'http://127.0.0.1:8000/files/img/c/preview/%D0%91%D0%B5%D0%B7_%D0%B8%D0%BC%D0%B5%D0%BD%D0%B8-1_EAhWMmE.webp', 'only_price_status': True, 'only_price': 3400, 'opt_price': None, 'opt_quantity': None, 'currency': 'RUB', 'status': 'stock', 'product_comp': [], 'brand': {'id': 4, 'brand': 'M-WELD', 'image': 'http://127.0.0.1:8000/files/img/c/brand/m-weld.webp', 'carousel': True, 'description': ''}, 'propstrmodel': [{'id': 11604, 'name': 'Вес, кг', 'qname': None, 'value': '1'}], 'category': 'Химия для сварки', 'quantity': 2}]}


response = requests.post('http://127.0.0.1:8000/o/order/', json=json_data)

# Красивый вывод JSON с отступами
formatted_json = json.dumps(response.json(), indent=4, ensure_ascii=False)
print(formatted_json)