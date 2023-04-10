from django.core.management.base import BaseCommand, CommandError
from catalog.models import ProductModel
from content.models import WideBannersModel
from pathlib import Path
import os
from PIL import Image
from time import sleep


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass


products_qs = ProductModel.objects.all()

counter = 0

for qs in products_qs:
    counter += 1

    webp_img = f'{ qs.preview_image }'.replace('.jpg', '.webp').replace('.png', '.webp')

    source = f'{ BASE_DIR }/files/{ qs.preview_image }'
    destination = f"{ BASE_DIR }/files/{ webp_img }"
    new_path = destination.replace(f'{ BASE_DIR }/files/', '') # Remove absolute path

    try:
        # Convert image
        image = Image.open(source)
        image.save(destination, format="webp")

        # Update data
        print(f'[OK:FileChange] {qs.id}\t{qs.preview_image} => {new_path}')
        products_qs.filter(id=qs.id).update(preview_image=new_path)
        
        if qs.preview_image:
            os.remove(source)
    
    except FileNotFoundError:
        print(f'[ERR:FileNotFoundError] {qs.id}\t{source} => {destination}')
        products_qs.filter(id=qs.id).update(preview_image=new_path)

    except IsADirectoryError:
        print(f'[ERR:IsADirectoryError] {qs.id}\t{source} => {destination}')
