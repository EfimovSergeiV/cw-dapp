import json
import requests
import random
import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.template.loader import render_to_string
from orders.serializers import *
from orders.notice import *
from orders.utils import *
from orders.models import *

from django.core.mail import send_mail
from django.template.loader import render_to_string

from main.agent import send_alert_to_agent
from django.shortcuts import render

from orders.utils import *
from django.conf import settings
        
from sber.views import SberInterface
from dreamkas.views import DreamkasInterface


class OrderInfoView(APIView):
    """ Информация о заказе """
    
    def get(self, request, order):
        # order_number = request.data["orderNumber"]
        order = CustomerModel.objects.get(order_number=order.upper())
        serializer = SmOrderListSerializer(order, context={'request':request})
        if order:
            return Response(serializer.data)
        else:
            return Response({ "error": "Заказ не найден" })


class RegisterPaymentView(APIView):
    """ Регистрация оплаты заказа """
    
    def post(self, request):
        order_number = request.data["orderNumber"]

        order = CustomerModel.objects.get(order_number=order_number.upper())
        if order.per_online_pay:
            register_data = SberInterface.payment_register(amount=order.total, order_number=order.order_number)
            print(register_data)
            try:
                order_id = register_data["orderId"]
                CustomerModel.objects.filter(order_number=order_number).update(payment_uuid=order_id)
            except KeyError:
                return Response({"error": "Сервис оплаты временно не доступен"})
            print(register_data)
            return Response(register_data)
        else:
            return Response({"error": "Оплата онлайн будет доступна после проверки заказа"})
        

class CheckOrderPaymentView(APIView):
    """" Проверка оплаты заказа """
    serializer_class = CustomerSerializer

    def post(self, request):
        try:
            # Проверка оплаты заказа
            order_id = request.data["orderId"]
            payment_data = SberInterface.payment_data(order_id)
            paymentAmountInfo = payment_data["paymentAmountInfo"]
            if paymentAmountInfo["paymentState"] == "DEPOSITED":

                # Отправляем на фискализацию и ставим статус оплаты в заказе
                order = CustomerModel.objects.filter(payment_uuid=order_id)
                serializer = QOrderListSerializer(order[0], context={'request':request})
                if not order[0].online_pay:
                    order.update(online_pay=True)
                    receipt_data = DreamkasInterface.generate_receipt(serializer.data)
                    receipt_result = DreamkasInterface.receipting_dreamkas(receipt_data)
                    print(receipt_result)

                    # Отправляем уведомлнеие в агент
                    payment = { "order_number": order[0].order_number, "total": order[0].total, "payment_uuid": order_id }
                    # send_alert_to_agent(payment=payment)
                    
                else:
                    order.update(online_pay=False)


            return Response(payment_data)
        except KeyError:
            return Response({ "error": "Не были предоставлены данные" })


""" Изменение статуса заказа отработанный или не отработанный """
def edit_order_status(request, uuid, status):
    post = "Заказ успешно помечен"
    qs = CustomerModel.objects.filter(uuid=uuid).update(status=status)
    if qs == 0:
        post = "Заказ не найден в системе"
    return render(request, 'questionclosed.html', { 'post': post})


class OrderListViews(APIView):
    """ Заказы пользователя """
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        user = request.user
        
        orders = CustomerModel.objects.filter(email=user.email)
        # Добавить в QS фильтер по телефону или другую мех. для сбора ВСЕХ заказов пользователя
        # all_order = CustomerModel.objects.filter(=user.email)
        # print(all_order)

        serializer = self.serializer_class(orders, many=True, context={"request": request})
        return Response(serializer.data)


class OrderViews(APIView):
    """ Обработка заказов """
    serializer_class = CustomerSerializer

    def post(self, request, format=None):
        """ Извлечение данных и структурирование заказа """
        data=request.data
        region_code = data.pop('region_code')
        select_shop = data.pop('shop_id')

        # Определяем стоимость товара исходя из выбранного магазина
        # Закидываем с ключём price в объект data
        for client_product in data['client_product']:
            for price in client_product['prod_price']:
                if price['shop'] == select_shop:
                    client_product['price'] = price['price']
            client_product['product_id'] = int(client_product['id'])

        # Присвоение кода и вычисление суммы по позициям заказа
        data['order_number'] = region_code + str(random.randrange(1000000, 1999999))
        data['position_total'] = get_position_summ(data['client_product'])

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()

            # Логика оповещений
            # send_alert_to_agent(order=serializer.data)
            mail_list = [
                # 'shop@glsvar.ru',
                ]

            if serializer.data['email']:
                mail_list.append(serializer.data['email'])

            OrderMails.send_notice(email=mail_list, data=serializer.data)
            return Response({ 'order': data['order_number'] })
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderStatusViews(APIView):
    """ Запрос статуса заказа """

    def post(self, request):
        code = request.data['code'] if request.data['code'] else None

        if code and 4 < len(code) < 10:
            order_qs = CustomerModel.objects.filter(order_number=code)
            
            try:
                status_name = order_qs[0].status
            except IndexError:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            return Response({"status": status_name })

        return Response(status=status.HTTP_400_BAD_REQUEST)


class RequestPriceViews(APIView):
    """ Запрос цены на товар """

    def post(self, request):
        data = request.data
        serializer = RequestPriceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            send_alert_to_agent(pricerequest=serializer.data)
            return Response(serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)



class MailsView(APIView):
    """ """
    def get(self, request):
        mail = False
        count = 0
        if mail:
            html_content = render_to_string('neuesJahr.html',)

            with open('list.txt') as file:
                mail_adress = file.read().lower().splitlines()

            for mail in mail_adress:
                
                count += 1
                send_mail(
                    'ООО Техносвар КС поздравляет Вас с новым годом!',
                    message=html_content,
                    from_email= 'market1@tehnosvar.ru',
                    recipient_list= [f'{mail}',],
                    fail_silently=False,
                    html_message=html_content
                    )
                print(count, mail)
                time.sleep(random.randrange(10, 20)) # Пробуем обойти спам

        return Response('Письмо отправлено')



@login_required
def send_payment_email(request, uuid):
    """ Отправка письма об оплате """
    try:
        order = CustomerModel.objects.get(uuid=uuid)
        html = "<html><body><h1>Письмо успешно отправлено</h1></br><a href='/a/orders/customermodel/'>Вернуться в админ панель</a></body></html>"
        html_content = render_to_string('permission_payment.html', {
                'order_number': order.order_number,
                'payment_link': f'{ settings.GLSVAR_FRONT }/payment?order={ order.order_number }',
                'total': order.total,
        })

        send_mail(
            f'Вы можете оплатить ваш заказ {order.order_number}',
            message=html_content,
            from_email= 'shop@glsvar.ru',
            recipient_list= [f'{order.email}',],
            fail_silently=False,
            html_message=html_content
            )
        return HttpResponse(html)
    except CustomerModel.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)


# def mail_template(request):
#     """ DEV VERSION """
#     # order = CustomerModel.objects.filter(delivery=True)[0]
#     order = CustomerModel.objects.get(uuid='5eed5115-51f1-481f-94d2-3ac6c4b10f1e')

#     return render(request, 'permission_payment.html', {
#             'order_number': order.order_number,
#             'payment_link': f'https://3dsec.sberbank.ru/payment/merchants/sbersafe_sberid/payment_ru.html?mdOrder={ order.uuid }/',
#             'total': order.total,
#         })