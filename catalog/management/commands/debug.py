from django.core.management.base import BaseCommand, CommandError
from catalog.models import *
import xlsxwriter, requests
from pathlib import Path

import json
from user.models import UserWatcherModel
from time import sleep


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


watchers = UserWatcherModel.objects.all()
print(watchers.values())