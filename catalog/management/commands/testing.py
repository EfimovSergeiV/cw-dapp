from django.core.management.base import BaseCommand, CommandError
from catalog.models import *

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


queryset = ProductModel.objects.filter(activated=True)

"""
qs = qs.filter(
    propstrmodel__qname=prop[0:4], 
    propstrmodel__qvalue=str(props[prop][0])
)
"""

queryset = queryset.filter(
    propstrmodel__qname= 'pa0s',
    propstrmodel__qvalue__in=['TIG']
)



for qs in queryset:
    print(qs)

print(len(queryset))