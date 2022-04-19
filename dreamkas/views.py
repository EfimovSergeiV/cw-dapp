# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

# from dreamkas.models import ReceiptsStatusModel
# from dreamkas.handlers import * # Узнать как инициализзировать 


# class DreamkasInterface:
#     """ Методы для взаимодействия интерфейса Deamkas """

#     def generate_receipt(order):
#         """ Генерация данных чека  """

#         uuid = ReceiptsStatusModel.objects.create()

#         # Получаем список товаров из базы продуктов Dreamkas
#         positions = []
#         for product_OrderDict in order['client_product']:
#             product = dict(product_OrderDict)
#             dreamkas_product = DreamkasProductModel.objects.get(association = product['product_id'])

#             positions.append({
#                 "remId": str(dreamkas_product.id),
#                 "name": product['name'],
#                 "type": dreamkas_product.type,
#                 "quantity": product['quantity'],
#                 "price": int(product['price'] + '00'), 
#                 "priceSum": int(product['price'] + '00') * product['quantity'],
#                 "tax": dreamkas_product.tax,
#             })

#         data = {
#             "externalId": str(uuid.externalId),
#             "deviceId": settings.DREAMKAS_DEVICE_ID,
#             "type": "SALE",
#                 "timeout": 5,
#             "taxMode": "DEFAULT",
#             "positions": positions,
#             "payments": [
#                 {
#                 "sum": int(str(order['position_total']) + '00'),
#                 "type": "CASHLESS"
#                 }
#             ],
#                 # "tags": [
#                 #     {
#                 #     "tag": 1212,
#                 #     "value": 12
#                 #     }
#                 # ],
#             "attributes": {
#                 "email": order['email'],
#                 "phone": order['phone'],
#             },
#             "total": {
#                 "priceSum":  int(str(order['position_total']) + '00'),
#             }
#         }

#         print(data)
#         return data


#     def receipting_dreamkas(data):
#         """
#         Фискализует чек в системе оплаты
#         """
#         payload = json.dumps(data)

#         headers = { 
#             'Content-Type': 'application/json',
#             'Authorization': f'Bearer { settings.DREAMKAS_TOKEN }',
#         }
#         response = requests.request(
#             method='POST',
#             url = f'{settings.DREAMKAS_API_URL}/receipts/',
#             headers=headers,
#             data = payload
#         )

#         data = response.json()
#         check = ReceiptsStatusModel.objects.filter(externalId=data['externalId'])

#         if check.exists() and data['status'] in ['SUCCESS', 'ERROR', 'IN_PROGRESS', 'PENDING']:
#             check.update(id=data['id'], createdAt=data['createdAt'] ,status=data['status'])

#         return data


# class UpdateReceiptsStatusWebhook(APIView):
#     """ Статусы фискализации чеков """

#     def post(self, request):
#         print(request.data['externalId'])
#         check = ReceiptsStatusModel.objects.filter(externalId=request.data['externalId'])
#         print(len(check))
#         if check.exists() and request.data['status'] in ['SUCCESS', 'ERROR', 'IN_PROGRESS', 'PENDING']:
#             check.update(status=request.data['status'])
#             return Response(status=HTTP_200_OK)

#         return Response(data="Чек не найден" ,status=HTTP_400_BAD_REQUEST)
