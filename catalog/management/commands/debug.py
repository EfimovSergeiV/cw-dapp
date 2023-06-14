from django.core.management.base import BaseCommand, CommandError
from catalog.models import *
import xlsxwriter
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


qss = ReviewsModel.objects.all()

for qs in qss:
    print(f'{qs.id}. {qs.name} {qs.image}')