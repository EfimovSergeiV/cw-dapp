"""
  Фиксим стоимость товаров, для корректной фильтрации по цене
"""

from django.core.management.base import BaseCommand
from catalog.models import ProductModel


class Command(BaseCommand):
    args = ''
    help = ''

    queryset = ProductModel.objects.all()

    def handle(self, *args, **options):
        pass

from time import sleep

products = ProductModel.objects.all()

for product in products:

    if product.only_price == 0:
        products.filter(id=product.id).update(only_price=None)
        # product.save()
    print(product.id, product.only_price)