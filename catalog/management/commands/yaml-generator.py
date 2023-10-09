from django.core.management.base import BaseCommand, CommandError
from catalog.models import ProductModel
from django.shortcuts import render

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


products = ProductModel.objects.filter(activated=True)

offer = f"""
<offer id="9012">
    <name>Мороженица Brand 3811</name>
    <vendor>Brand</vendor>
    <vendorCode>A1234567B</vendorCode>
    <url>http://best.seller.ru/product_page.asp?pid=12345</url>
    <price>8990</price>
    <oldprice>9990</oldprice>
    <enable_auto_discounts>true</enable_auto_discounts>
    <currencyId>RUR</currencyId>
    <categoryId>101</categoryId>
    <picture>http://best.seller.ru/img/model_12345.jpg</picture>
    <description>
        <![CDATA[          
            <p>Это прибор, который придётся по вкусу всем любителям десертов и сладостей</p>
            <p>С его помощью вы сможете делать вкусное домашнее мороженое из натуральных ингредиентов.</p>
        ]]>
    </description>                
    <sales_notes>Необходима предоплата.</sales_notes>
    <manufacturer_warranty>true</manufacturer_warranty>
    <barcode>4601546021298</barcode>
    <param name="Цвет">белый</param>
    <weight>3.6</weight>
    <dimensions>20.1/20.551/22.5</dimensions>
    <condition type="preowned">
        <quality>excellent</quality>
    </condition>
</offer>
"""

template = f"""
<?xml version="1.0" encoding="UTF-8"?>
<yml_catalog date="2020-11-22T14:37:38+03:00">
    <shop>
        <name>BestSeller</name>
        <company>Tne Best inc.</company>
        <url>http://best.seller.ru</url>
        <platform>uCoz</platform>
        <categories>
            <category id="1">Бытовая техника</category>
            <category id="10" parentId="1">Мелкая техника для кухни</category>
            <category id="101" parentId="10">Сэндвичницы и приборы для выпечки</category>
        </categories>
        <delivery-options>
            <option cost="200" days="1"/>
        </delivery-options>
        <pickup-options>
            <option cost="200" days="1"/>
        </pickup-options>
        <offers>

            <offer id="9012">
                <name>Мороженица Brand 3811</name>
                <vendor>Brand</vendor>
                <vendorCode>A1234567B</vendorCode>
                <url>http://best.seller.ru/product_page.asp?pid=12345</url>
                <price>8990</price>
                <oldprice>9990</oldprice>
                <enable_auto_discounts>true</enable_auto_discounts>
                <currencyId>RUR</currencyId>
                <categoryId>101</categoryId>
                <picture>http://best.seller.ru/img/model_12345.jpg</picture>
                <description>
                    <![CDATA[          
                        <p>Это прибор, который придётся по вкусу всем любителям десертов и сладостей</p>
                        <p>С его помощью вы сможете делать вкусное домашнее мороженое из натуральных ингредиентов.</p>
                    ]]>
                </description>                
                <sales_notes>Необходима предоплата.</sales_notes>
                <manufacturer_warranty>true</manufacturer_warranty>
                <barcode>4601546021298</barcode>
                <param name="Цвет">белый</param>
                <weight>3.6</weight>
                <dimensions>20.1/20.551/22.5</dimensions>
                <condition type="preowned">
                    <quality>excellent</quality>
                </condition>
            </offer>

        </offers>
    </shop>
</yml_catalog>
"""

print(template)

for product in products[0:2]:
    print(product.name)