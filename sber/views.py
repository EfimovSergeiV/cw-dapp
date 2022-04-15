import json
import requests
from sber.models import *
from django.conf import settings


class SberMethods:
    """ Список методов Сбера """

    def gateway(method, payload ) -> json:
        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        url = f'{ settings.SBER_API_URL }/{ method }'

        payload["userName"] = settings.SBER_USERNAME
        payload["password"] = settings.SBER_PASSWORD
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()

    def register(order_number, amount) -> dict[str, dict]:
        """ Регистрация заказа в эквайринге """

        method = 'register.do'
        payload = {
            "orderNumber": order_number,
            "amount": int(str(amount) + '00'),
            "returnUrl": settings.SBER_RETURN_URL,
            "failUrl": settings.SBER_FAIL_URL,
        }
        return { "method": method, "payload": payload }

    def get_order_status_extended(order_id) -> dict[str, dict]:
        """ Проверка статуса оплаты """

        method = 'getOrderStatusExtended.do'
        payload = {
            "orderId": order_id,
        }
        return { "method": method, "payload": payload }


# class OrderData:
#     """ Методы работы с заказами """

#     def search_order(order_number=None, order_id=None) -> dict:
#         """ Поиск заказов """
#         if order_number:
#             order = CustomerModel.objects.get(order_number=order_number.upper())
#         if order_id:
#             order = CustomerModel.objects.get(order_id=order_id)

#         total = str(order.total + order.delivery_summ)
#         amount = total + '00'

#         return {
#             "amount": amount,
#             "orderId": order.payment_uuid,
#             "orderNumber": order_number,
#         }


# class RegisterView(APIView):
#     """ Регистрация заказа для оплаты """

#     def post(request):
#         try:

#             order_number = request.data["orderNumber"]
#             order = OrderData.search_order(order_number=order_number)
#             form = SberMethods.register(amount=order["amount"], order_number=order["orderNumber"])
#             response = SberMethods.gateway(method=form['method'], payload=form['payload'])
#             CustomerModel.objects.filter(order_number=order_number).update(payment_uuid=response['orderId'])

#             return Response(response)

#         except KeyError:
#             return Response({ "error": "Не были предоставлены данные" })


# class StatusView(APIView):
#     """ 
#     Проверка оплаты
#     """

#     def post(request):
#         try:
#             order_id = request.data["orderId"]
#             form = SberMethods.get_order_status_extended(order_id=order_id)
#             response = SberMethods.gateway(method=form['method'], payload=form['payload'])

#             payment = response['paymentAmountInfo']
            
#             if payment['paymentState'] == 'DEPOSITED':
#                 order = CustomerModel.objects.filter(payment_uuid=order_id)
                
#                 payment = { "order_number": order[0].order_number, "total": order[0].total, "payment_uuid": order_id }
                
#                 # send_alert_to_agent(payment=payment)

#                 order.update(online_pay=True)
#             return Response(response)

#         except KeyError:
#             return Response({ "error": "Не были предоставлены данные" })


# class ContinueView(APIView):
#     """ Продолжение прерванной оплаты """

#     def post(request):
#         order_number = request.data['orderNumber']
#         order = OrderData.search_order(order_number=order_number)
#         print(order)
#         if order['orderId']:
#             return Response({ "orderId": order.payment_uuid })

#         else:
#             form = SberMethods.register(amount=order["amount"], order_number=order["orderNumber"])
#             response = SberMethods.gateway(method=form['method'], payload=form['payload'])
#             CustomerModel.objects.filter(order_number=order_number).update(payment_uuid=response['orderId'])

#             return Response(response)



""" Интерфейс для работы с эквайрингом """
class SberInterface:
    """ Список методов Сбера """
    #PR: Убрать дублирование кода

    def payment_register(amount, order_number=None):
        try:
            form = SberMethods.register(amount=amount, order_number=order_number)
            try:
                response = SberMethods.gateway(method=form['method'], payload=form['payload'])
            except requests.exceptions.SSLError:
                return { "error": "Сервис оплаты временно не доступен" }
            return response

        except KeyError:
            return { "error": "Не были предоставлены данные" }

    def payment_data(order_id):
        """ Получение данных оплаты """
        try:
            form = SberMethods.get_order_status_extended(order_id=order_id)
            try:
                response = SberMethods.gateway(method=form['method'], payload=form['payload'])
                print(response)
            except requests.exceptions.SSLError:
                return { "error": "Сервис оплаты временно не доступен" }
            return response
        except KeyError:
            return { "error": "Не были предоставлены данные" }
