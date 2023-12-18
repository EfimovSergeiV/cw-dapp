from django.core.management.base import BaseCommand, CommandError
from catalog.models import ProductModel
from django.shortcuts import render

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


products = ProductModel.objects.filter(id__in = [ 312, 313, 314, 315, 316, 317, 318, 319 ])


offers = ''
offer_template = """\n      <offer id="{id}">
        <name>{name}</name>
        <vendor>{brand}</vendor>
        <vendorCode>{vcode}</vendorCode>
        <url>https://www.glsvar.ru/product/{id}</url>
        <price>{price}</price>
        <currencyId>RUB</currencyId>
        <categoryId>{ct_id}</categoryId>
        <picture>https://api.glsvar.ru/files/{picture}</picture>
        <description>
          <![CDATA[          
            <p>{description}</p>
          ]]>
        </description>
      </offer>\n"""



for product in products:
    offer = offer_template.format(
        name = product.name,
        brand = product.brand,
        vcode = product.vcode,
        id = product.id,
        price = int(product.only_price),
        ct_id = product.category_id,
        picture = product.preview_image,
        description = product.description,
    )
    offers += offer
    print(offer)


# print(offers)


yml_template = """<?xml version="1.0" encoding="UTF-8"?>
  <yml_catalog date="2023-12-15T12:00:00+03:00">
  <shop>
    <name>Главный Сварщик</name>
    <company>Главный Сварщик</company>
    <url>https://glsvar.ru</url>
    <email>zakaz@glsvar.ru</email>
    <currencies>
      <currency id="RUB" rate="1"></currency>
    </currencies>
    <categories>
      <category id="31">Сварочные электроды</category>
    </categories>
    <offers>
{offers}
    </offers>
  </shop>
</yml_catalog>
"""



with open(f'./esab-elektrods.xml', 'w' ) as file:
    file.write(
        yml_template.format(
            offers = offers
        )
    )

for product in products:
    print(f'{int(product.only_price)} руб. - {product.name}')