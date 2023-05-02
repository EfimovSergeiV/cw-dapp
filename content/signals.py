""" Это работает юлагодаря тому, что мы импортируем это в представлениях """

import json
import requests

from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save, pre_save
from content.models import ReviewsModel
from PIL import Image


@receiver(post_save, sender=ReviewsModel)
def create_or_update(sender, **kwargs):
    """ Создание или редактирование товара в Dreamkas """
    image = f'{ settings.BASE_DIR }/files/{kwargs["instance"].image}'
    print(f'{ image }')
    print(f'{ image.replace(".webp", "-static.webp")}')
    static_image = f'{ image.replace(".webp", "-static.webp")}'

    image = Image.open(image)
    image.save(static_image, format="webp")

#     serializer = DreamkasProductSerializer(kwargs['instance'])
#     payload = json.dumps(serializer.data)

#     response = requests.request(
#         method='GET',
#         url=f'{settings.DREAMKAS_API_URL}/products/{kwargs["instance"].id}',
#         headers=headers
#     )

#     if response.status_code == 200:
#         # Обновление товара
#         response = requests.request(
#             method='PATCH',
#             url=f'{settings.DREAMKAS_API_URL}/products/{kwargs["instance"].id}',
#             headers=headers,
#             data=payload
#         )
#     elif response.status_code == 404:
#         # Создание товара
#         response = requests.request(
#             method='POST',
#             url=f'{settings.DREAMKAS_API_URL}/products/',
#             headers=headers,
#             data=payload
#         )
#     else:
#         raise Exception(f'Ошибка при создании товара: {response.status_code}')


# @receiver(post_delete, sender=DreamkasProductModel)
# def delete(sender, **kwargs):
#     """ Удаление товара в Dreamkas """

#     requests.request(
#         "DELETE", 
#         url=f'{settings.DREAMKAS_API_URL}/products/{kwargs["instance"].id}',
#         headers=headers)