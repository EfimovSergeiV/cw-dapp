import json
import requests

from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_delete, post_save, pre_save
# #Заюзать pre_save для подтигивания данных о товаре

from dreamkas.models import DreamkasProductModel
from dreamkas.serializers import DreamkasProductSerializer


headers = { 
    'Content-Type': 'application/json',
    'Authorization': f'Bearer { settings.DREAMKAS_TOKEN }',
}

@receiver(post_save, sender=DreamkasProductModel)
def create_or_update(sender, **kwargs):
    """ Создание или редактирование товара в Dreamkas """

    serializer = DreamkasProductSerializer(kwargs['instance'])
    payload = json.dumps(serializer.data)

    response = requests.request(
        method='GET',
        url=f'{settings.DREAMKAS_API_URL}/products/{kwargs["instance"].id}',
        headers=headers
    )

    if response.status_code == 200:
        # Обновление товара
        response = requests.request(
            method='PATCH',
            url=f'{settings.DREAMKAS_API_URL}/products/{kwargs["instance"].id}',
            headers=headers,
            data=payload
        )
    elif response.status_code == 404:
        # Создание товара
        response = requests.request(
            method='POST',
            url=f'{settings.DREAMKAS_API_URL}/products/',
            headers=headers,
            data=payload
        )
    else:
        raise Exception(f'Ошибка при создании товара: {response.status_code}')


@receiver(post_delete, sender=DreamkasProductModel)
def delete(sender, **kwargs):
    """ Удаление товара в Dreamkas """

    requests.request(
        "DELETE", 
        url=f'{settings.DREAMKAS_API_URL}/products/{kwargs["instance"].id}',
        headers=headers)