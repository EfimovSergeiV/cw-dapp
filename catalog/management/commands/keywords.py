from os import cpu_count
from django.core.management.base import BaseCommand
from catalog.models import *

from django.db.models.functions import Lower
from django.db.models import CharField

"""

ПАРСЕР КЛЮЧЕВЫХ СЛОВ С ЗАПИСЬЮ/ПЕРЕЗАПИСЬЮ В ProductModel.keywords

"""

CharField.register_lookup(Lower)
class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


wordkey_brand = {
    "SCOMES" : [ 'scomes', 'скомес' ],
    "EWM" : [ 'ewm', 'евм' ],
    "MONOLITH" : [ 'monolith', 'монолит' ],
    "Lincoln Electric" : [ 'lincoln electric', 'линкольн электрик' ],
    "Denzel" : [ 'dencel', 'денцель'],
    "Integral" : [ 'integral', 'интеграл'],
    "Aurora" : ['aurora', 'аврора' ],
    "Krasniy Stakan" : [ 'krasniy stakan', 'красный стакан', ],
    "Arrow Solutions" : [ 'arrow solutions', 'арров солюшн'],
    "GCE" : [ 'gse', 'гсе' ],
    "Оливер" : [ 'oliver', 'оливер' ],
    "Химавангард" : [ 'himavangard', 'химавангард' ],
    "ASOIK" : [ 'asoik', 'асоик' ],
    "Главный сварщик" : [ 'главный сварщик', 'chief welder' ],
    "HUTER" : ['huter', 'хутер'],
    "EUROLUX" : [ 'eurolux', 'евролюкс' ],
    "TELWIN" : [ 'telwin', 'телвин' ],
    "FARINA" : [ 'farina', 'фарина' ],
    "KOBELCO" : [ 'kobelco', 'кобелсо' ],
    "Кедр" : [ 'kedr', 'кедр' ],
    "Сварог" : [ 'svarog', 'сварог' ],
    "PlasmaTEC" : [ 'plasmatec', 'плазматех' ],
    "MEGMEET" : [ 'megmeet', 'мигмет' ],
    "Ресанта" : [ 'resanta' , 'ресанта' ],
    "Форсаж" : ['forsash', 'форсаж' ],
    "M-WELD" : ['m-weld', 'м-велд' ],
    "ESAB" : [ 'esab', 'есаб' ],
    "Редиус" : [ 'redius', 'редиус'],
    "FUBAG" : [ 'fubag', 'фубаг' ],
}


qs_prods = ProductModel.objects.all()
count = 0

for product in qs_prods:   
    if product.brand is not None:

        brand = wordkey_brand[str(product.brand)]
        keywords = brand[0] + ', ' + brand[1]
        print(keywords)
        qs_prods.filter(name=product.name).update(keywords=keywords)
