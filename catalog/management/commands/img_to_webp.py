from django.core.management.base import BaseCommand, CommandError
from catalog.models import ProductModel
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


products_qs = ProductModel.objects.filter(activated=True)


for qs in  products_qs:

    file = f'{qs.preview_image}'.replace('.jpg', '.webp').replace('.png', '.webp')

    print(file)

# for qs in products_qs:

#     source = f'{ BASE_DIR }/files/{ qs.preview_image }'
#     destination = f"{ BASE_DIR }/{ file }"

#     # Convert image
#     image = Image.open(source)
#     image.save(destination, format="webp")

#     # Update data
#     new_path = destination.replace(f'{ BASE_DIR }/files/', '')
#     banners_qs.filter(id=qs.id).update(preview_image=new_path)

#     print(f'\n{source}\n{destination}')

#     os.remove(source)
