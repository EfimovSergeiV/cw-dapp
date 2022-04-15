
import json
import requests
from django.conf import settings
from dreamkas.models import ReceiptsStatusModel, DreamkasProductModel

"""
Мост для соединения эквайринга ,онлайн-кассы Dreamkas и Веб-приложением
Отправляет данные для прохождения оплаты пользователем, фискализует чеки и 
уведомляет об результатах прохождения оплаты пользователем
"""

headers = { 
    'Content-Type': 'application/json',
    'Authorization': f'Bearer { settings.DREAMKAS_TOKEN }',
}

def generate_order(order=None):
    """
    Генерирует новый заказ в системе оплаты
    Возвращает объект заказа
    !!! Внимание из OrderDict
    """

    # uuid = create_receipts_entry(order['uuid'])
    uuid = ReceiptsStatusModel.objects.create()

    # Получаем список товаров из базы продуктов Dreamkas
    positions = []
    for product_OrderDict in order['client_product']:
        product = dict(product_OrderDict)
        dreamkas_product = DreamkasProductModel.objects.get(association = product['product_id'])

        positions.append({
            "remId": str(dreamkas_product.id),
            "name": product['name'],
            "type": dreamkas_product.type,
            "quantity": product['quantity'],
            "price": int(product['price'] + '00'), 
            "priceSum": int(product['price'] + '00') * product['quantity'],
            "tax": dreamkas_product.tax,
        })

    data = {
        "externalId": str(uuid.externalId),
        "deviceId": settings.DREAMKAS_DEVICE_ID,
        "type": "SALE",
            "timeout": 5,
        "taxMode": "DEFAULT",
        "positions": positions,
        "payments": [
            {
            "sum": int(str(order['total']) + '00'),
            "type": "CASHLESS"
            }
        ],
            # "tags": [
            #     {
            #     "tag": 1212,
            #     "value": 12
            #     }
            # ],
        "attributes": {
            "email": order['email'],
            "phone": order['phone'],
        },
        "total": {
            "priceSum":  int(str(order['total']) + '00'),
        }
    }

    return data


def receipting_dreamkas(data):
    """
    Фискализует чек в системе оплаты
    """
    payload = json.dumps(data)

    headers = { 
        'Content-Type': 'application/json',
        'Authorization': f'Bearer { settings.DREAMKAS_TOKEN }',
    }
    response = requests.request(
        method='POST',
        url = f'{settings.DREAMKAS_API_URL}/receipts/',
        headers=headers,
        data = payload
    )

    data = response.json()
    check = ReceiptsStatusModel.objects.filter(externalId=data['externalId'])

    if check.exists() and data['status'] in ['SUCCESS', 'ERROR', 'IN_PROGRESS', 'PENDING']:
        check.update(id=data['id'], createdAt=data['createdAt'] ,status=data['status'])

    return data


""" Тестируем с QS """

def test_qs(order):
    print('THIS IS TESTING QS ', order)
    return order