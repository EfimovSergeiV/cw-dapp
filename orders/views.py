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
from catalog.models import ProductModel
from orders.serializers import *
from orders.notice import *
from orders.utils import *
from orders.models import *

from django.core.mail import send_mail
from django.template.loader import render_to_string

from main.agent import send_alert_to_agent, one_click_order_to_agent
from main.mattermost import mattermost_notification

from django.shortcuts import render

from orders.utils import *
from django.conf import settings
from datetime import datetime, timedelta

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


class OneSotfOrderView(APIView):
    """ Информация о заказе для 1С Bad decision"""
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        
        now = datetime.now()
        orders = CustomerModel.objects.filter(date_created__gte=now - timedelta(days=1))
        serializer = OneSoftOrderSerializer(orders, many=True, context={'request':request})

        return Response(serializer.data)


class RegisterPaymentView(APIView):
    """ Регистрация оплаты заказа """
    
    def post(self, request):
        order_number = request.data["orderNumber"]

        order = CustomerModel.objects.get(order_number=order_number.upper())
        if order.per_online_pay:
            register_data = SberInterface.payment_register(amount=order.total, order_number=order.order_number)
            print(register_data)
            try:
                if 'errorCode' in register_data.keys():
                    return Response({ "error": "Заказ с таким номером уже обработан" })
                else:
                    order_id = register_data["orderId"]
                    CustomerModel.objects.filter(order_number=order_number).update(payment_uuid=order_id)

            except KeyError:
                return Response({"error": "Сервис оплаты временно не доступен"})

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
                    pass
                    # order.update(online_pay=False)


            return Response(payment_data)
        except KeyError:
            return Response({ "error": "Не были предоставлены данные" })


""" Изменение статуса заказа отработанный или не отработанный """
def edit_order_status(request, uuid, status):
    # send_alert_to_agent(order=serializer.data)

    ORDER_STATUS = {
        "notprocessed": "не обработан",
        "inprocessed": "в обработке",
        "processed": "обработан",
        "awaitingpayment": "ожидает оплаты",
        "delivery": "доставка ТК",
        "waitingclient": "ожидает клиента",
        "completed": "выполнен",
        "notcompleted": "не выполнен",
    }

    
    qs = CustomerModel.objects.filter(uuid=uuid)
    try:
        if len(qs) == 1 and request.headers['Cookie']:

            if qs[0].status == status:
                post = f"Кто то уже дал заказу {qs[0].order_number} статус: {ORDER_STATUS[status]}"

            else:
                qs.update(status=status)
                send_alert_to_agent(status = { "order": qs[0].order_number, "status": ORDER_STATUS[status] })
                post = f"Статус заказа {qs[0].order_number} сменён на: {ORDER_STATUS[status]}"

        else:
            post = "Заказ не найден в системе"
        return render(request, 'questionclosed.html', { 'post': post})
    except:
        post = "Вы не прошли проверку на работа"
        return render(request, 'questionclosed.html', { 'post': post })


""" Изменение статусов обработки сообщений и запросов о стоимости товаров """
def price_request_status(request, uuid):
    qs = RequestPriceModel.objects.filter(uuid=uuid)
    
    # print(request.headers)
    # with open("requestHeaders.txt", 'w') as file:
    #     file.write(str(request.headers)) #

    try:
        if len(qs) == 1 and request.headers['Cookie']:
            if qs[0].completed:
                post = f"Вопрос клиента { qs[0].contact } кто-то уже взял на себя"
            else:
                qs.update(completed=True)
                post = f"Вопрос клиента { qs[0].contact } помечен как закрытый"
                send_alert_to_agent(oth_status = { "client": qs[0].contact })
    
        else:
            post = "Вопрос не найден в системе"

        return render(request, 'questionclosed.html', { 'post': post })
    except:
        post = "Вы не прошли проверку на работа"
        return render(request, 'questionclosed.html', { 'post': post })



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


from django.core.files.storage import FileSystemStorage
from serializers.catalog import ListProductsSerializer
from catalog.utils import CustomUtils, ChangeCurrency
from rest_framework.utils.serializer_helpers import ReturnDict
from django.core.exceptions import ObjectDoesNotExist
class OrderViews(APIView):
    """ Обработка заказов """
    serializer_class = CustomerSerializer

    def post(self, request, format=None):
        """ Извлечение данных и структурирование заказа """
        if request.content_type == 'application/json':
            data=request.data

            prods_id = [product['id'] for product in data['client_product']]
            products_qs = ProductModel.objects.filter(id__in=prods_id)#.values()

            # Присвоение кода и вычисление суммы по позициям заказа
            region_code = data.pop('region_code')            
            data['order_number'] = region_code + str(random.randrange(1000000, 1999999))

            # Проверка стоимости товаров
            products = data.pop('client_product')
            for product in products:
                try:
                    price_from_db = products_qs.get(id = product['id'])
                    product['product_id'] = product['id']
                    product["price"] = price_from_db.opt_price if product.get('opt') else price_from_db.only_price
                except ObjectDoesNotExist:
                    pass

            data['client_product'] = products
            data['position_total'] = get_position_summ(data['client_product'])
            data['total'] = get_position_summ(data['client_product'])

            # HotFix: Удаляем ключь если он не заполнен
            if data['delivery_adress'] == None:
                data.pop('delivery_adress')

            serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                serializer.save()

                # Логика оповещений
                try:
                    send_alert_to_agent(order=serializer.data)
                    mattermost_notification(template="order_template", data=serializer.data)
                except:
                    pass

                mail_list = [
                    # 'efimovsergeiv@gmail.com',
                    ]
                if serializer.data['email']:
                    mail_list.append(serializer.data['email'])
                OrderMails.send_notice(email=mail_list, data=serializer.data)

                return Response({ 'order': data['order_number'] })

            else:
                print(serializer.errors)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
        
        else:
            fs = FileSystemStorage()
            filename = fs.save(f'orders/{request.FILES["file"].name}', request.FILES["file"])

            # проверить заказ на дату
            CustomerModel.objects.filter(order_number=request.data['order_number']).update(file=filename)

            mattermost_notification(template="order_file_template", data={"url": f"https://api.glsvar.ru/files/{filename}"})
            return Response(status=status.HTTP_200_OK)
        


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
            
            print(serializer.data)
            send_alert_to_agent(pricerequest=serializer.data)

            # HotFix:
            mm_data = {
                "contact": serializer.data['contact'],
                "city": serializer.data['city'],
                "id": str(serializer.data['product']).split()[1],
                "product": serializer.data['product'],
            }
            mattermost_notification(template="request_template", data=mm_data)

            return Response(serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)





class MailsView(APIView):
    """ """
    def get(self, request):
        mail = True
        count = 0
        if mail:
            html_content = render_to_string('action.html',)

            with open('list.txt') as file:
                mail_adress = file.read().lower().splitlines()

            for mail in mail_adress:
                print(f'send to mail: { mail }')
                
                count += 1
                send_mail(
                    'Главный сварщик поздравляет с 23 февраля!',
                    message=html_content,
                    from_email= 'zakaz@glsvar.ru',
                    recipient_list= [f'{ str(mail) }',],
                    fail_silently=False,
                    html_message=html_content
                    )
                # print(count, mail)
                # time.sleep(random.randrange(10, 20)) # Пробуем обойти спам

        return Response('Письмо отправлено')






class PromocodeView(APIView):
    """ Проверка активного промокода """

    #  { "promo": "23Февраля" }

    def post(self, request):

        data = request.data
        promocode = data.get('promo')
        promo = PromocodeModel.objects.filter(promocode=promocode)

        if promo:
            return Response({ "discount": promo[0].value, "prods": promo[0].products.replace(' ', '').split(',') })
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)




@login_required
def send_payment_email(request, uuid):
    """ Отправка письма об оплате """
    try:
        order = CustomerModel.objects.get(uuid=uuid)
        products = OrderedProductModel.objects.filter(customer=order)
        html = "<html><body><h1>Письмо успешно отправлено</h1></br><a href='/a/orders/customermodel/'>Вернуться в админ панель</a></body></html>"
        html_content = render_to_string('permission_payment.html', {
                'order_number': order.order_number,
                'seller_comm': order.seller_comm,
                'delivery': order.delivery,
                'delivery_summ': order.delivery_summ,
                'payment_link': f'{ settings.GLSVAR_FRONT }/payment?order={ order.order_number }',
                'total': order.total,
                'client_product': products,
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



# Сумма заказа (OneClick)
def get_tolal(products):
    """ Вычисление суммы по позициям заказа """
    total = 0
    for product in products:
        total += product['price'] * product['quantity']
    return total


class OneClickOrderView(APIView):
    """ Оформление заказа в один клик """

    def post(self, request):
        
        map_region = {
            "Псков": "PSK",
        }

        # Присвоение кода и вычисление суммы по позициям заказа
        order_number = map_region[str(request.data.get("city"))] + str(random.randrange(1000000, 1999999))

        print(request.data)

        prod_type = request.data.get('prod_type')
        order = {
            "order_number": order_number,
            "name": request.data.get('name'),
            "contact": request.data.get('contact'),
            "msger": request.data.get('msger'),
            "shop": request.data.get('shop'),
            "comment": request.data.get('comment'),
            "total": get_tolal(request.data.get('prods')),
            "prods": request.data.get('prods'),
        }

        one_click_order_to_agent(order)
        mattermost_notification(template="one_click_order_template", data=order)

        return Response({ "order": order_number})



from orders.serializers import ReviewSerializer
class ReviewView(APIView):
    """ Отзывы к товарам """

    def get(self, request, id):
        reviews = ReviewModel.objects.filter(product_id=id, activated=True)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        data = request.data
        data['product_id'] = id
        data["user_name"] = data.get('user_name') if data.get('user_name') else 'Пользователь'
        serializer = ReviewSerializer(data=data)

        if serializer.is_valid() and data.get('rating') in range(1, 6):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)