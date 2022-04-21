import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from dreamkas.models import ReceiptsStatusModel
from dreamkas.handlers import * # Узнать как инициализзировать 


class DreamkasInterface:
    """ Методы для взаимодействия интерфейса Deamkas """

    def generate_receipt(order):
        """ Генерация данных чека  """

        uuid = ReceiptsStatusModel.objects.create()

        # Получаем список товаров из базы продуктов Dreamkas
        positions = []
        for product_OrderDict in order['client_product']:
            product = dict(product_OrderDict)

            # Создаёт товар в кассе, если он остутствует, с параметрами по умолчанию
            try:
                dreamkas_product = DreamkasProductModel.objects.get(association = product['product_id'])
            except DreamkasProductModel.DoesNotExist:
                DreamkasProductModel.objects.create(association = product['product_id'], name = product['name'])
                dreamkas_product = DreamkasProductModel.objects.get(association = product['product_id'])

            positions.append({
                "remId": str(dreamkas_product.id),
                "name": product['name'],
                "type": dreamkas_product.type,
                "quantity": product['quantity'],
                "price": int(product['price'] + '00'), 
                "priceSum": int(product['price'] + '00') * product['quantity'],
                "tax": dreamkas_product.tax,
                "tags": [
                    # {
                    #     "tag": 1214,
                    #     "value": 1
                    # },
                ],
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
                "sum": int(str(order['position_total']) + '00'),
                "type": "CASHLESS"
                }
            ],
                "tags": [
                    # {
                    #     "tag": 1212,
                    #     "value": 12
                    # },
                ],
            "attributes": {
                "email": order['email'],
                "phone": order['phone'],
            },
            "total": {
                "priceSum":  int(str(order['position_total']) + '00'),
            }
        }

        print(data)
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



class UpdateReceiptsStatusWebhook(APIView):
    """ Обработка вебхуков кассы dreamkas """

    def post(self, request):
        """ Запись данных в файлик """
        # dir = 'dreamkas/hooksdata/'
        # files = os.listdir(dir)
        # with open(f'{ dir }{ len(files) + 1 }.json', 'w') as f:
        #     data = request.data
        #     json_data = json.dumps(data)
        #     f.write(json_data)
        #     f.close()

        # try:
        #     print(request.data['externalId'])
        #     check = ReceiptsStatusModel.objects.filter(externalId=request.data['externalId'])
        #     print(len(check))
        #     if check.exists() and request.data['status'] in ['SUCCESS', 'ERROR', 'IN_PROGRESS', 'PENDING']:
        #         check.update(status=request.data['status'])
        #         return Response(status=HTTP_200_OK)

        #     return Response(data="Чек не найден" ,status=HTTP_400_BAD_REQUEST)
        # except:
        #     return Response(data="Чек не найден" ,status=HTTP_400_BAD_REQUEST)

        data = {'action': 'CREATE', 'type': 'RECEIPT', 'data': {'_id': '625fb3d68abd4b4998e58ad1', 'deviceId': 105404, 'userId': 98341, 'shopId': 148146, 'operationId': '625fb39b6637bc0018acd185', 'type': 'SALE', 'shiftId': 4, 'cashier': {'name': 'Кассир', '_id': '625fc1e692cc9d17b77e0e0c'}, 'number': 3, 'depth': 1, 'fiscalDocumentNumber': '28', 'fiscalDocumentSign': '3209733296', 'fnNumber': '9999078902003043', 'registryNumber': '0004494543062458', 'margin': 0, 'customer': {'email': 'efimovsergeiv@gmail.com'}, 'positions': [{'id': '6cba22ec-703e-4d77-81cf-92677ee59659', 'name': 'Силовой кабель КГ 1х16', 'type': 'COUNTABLE', 'unit': '796', 'price': 25700, 'quantity': 1000, 'amount': 25700, 'discount': 0, 'tax': 'NDS_20', 'margin': 0, 'alcVolumeMl': 1000, 'departmentId': None, 'discounts': []}], 'payments': [{'type': 'CASHLESS', 'amount': 25700}], 'discount': 0, 'amount': 25700, 'localDate': '2022-04-20T10:18:37.000Z', 'date': '2022-04-20T07:18:37.000Z'}}

        print(request.data)
        return Response(status=HTTP_200_OK)
