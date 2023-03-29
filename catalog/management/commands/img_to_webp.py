from django.core.management.base import BaseCommand, CommandError
from catalog.models import *
from content.models import WideBannersModel
from pathlib import Path
import os
from PIL import Image


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


banners_qs = WideBannersModel.objects.all()

for qs in banners_qs:

    source = f'{ BASE_DIR }/files/{ qs.image }'
    destination = f"{ source.replace('.jpg', '.webp') }"

    # Convert image
    image = Image.open(source)
    image.save(destination, format="webp")

    # Update data
    new_path = destination.replace(f'{ BASE_DIR }/files/', '')
    banners_qs.filter(id=qs.id).update(image=new_path)

    print(f'\n{source}\n{destination}')

    os.remove(source)
