from django.core.management.base import BaseCommand, CommandError
from catalog.models import ProductModel
from django.shortcuts import render
from datetime import datetime

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


products = ProductModel.objects.filter(id__in = [1989, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 2004, 2003,])
current_datetime = datetime.now()
formatted_date = current_datetime.strftime("%Y-%m-%dT%H:%M:%S")


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
        <delivery>false</delivery>
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

    if int(product.only_price) > 0:
      offers += offer
      print(offer)



yml_template = """<?xml version="1.0" encoding="UTF-8"?>
  <yml_catalog date="{current_date}+03:00">
  <shop>
    <name>Главный Сварщик</name>
    <company>Главный Сварщик</company>
    <url>https://glsvar.ru</url>
    <email>zakaz@glsvar.ru</email>
    <currencies>
      <currency id="RUB" rate="1"></currency>
    </currencies>
    <categories>
      <category id="109">Сварочные краги и перчатки</category>
      <category id="110">Акции главного сварщика</category>
    </categories>
    <offers>
{offers}
    </offers>
  </shop>
</yml_catalog>
"""



with open(f'./glsvar-krags.xml', 'w' ) as file:
    file.write(
        yml_template.format(
            current_date = formatted_date,
            offers = offers
        )
    )

for product in products:
    print(f'{int(product.only_price)} руб. - {product.name}')