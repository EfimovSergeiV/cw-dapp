from cgi import print_environ
from itertools import count
from traceback import print_tb
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


import json
import requests
from main.models import DeleviryServiceModel
from orders.cdek import *
#import datetime


tokens = {
    # "cdek": {
    #     "token": 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZSI6WyJvcmRlcjphbGwiLCJwYXltZW50OmFsbCJdLCJleHAiOjE2NDQyMzY1ODYsImF1dGhvcml0aWVzIjpbImNvbnRyYWdlbnQtdXVpZDplNDM2MzJkNy1hNDdhLTQwNjYtOTk0NC04OGFjZDdmYzUxMTQiLCJhY2NvdW50LWxhbmc6cnVzIiwiY2xpZW50LWlkLWVjNTplNDM2MzJkNy1hNDdhLTQwNjYtOTk0NC04OGFjZDdmYzUxMTQiLCJhcGktdmVyc2lvbjoyLjAiLCJzaGFyZC1pZDpydS0wMiIsImNvbnRyYWN0OtCY0Jwt0KDQpC3QltCd0J4tNDMxIiwiYWNjb3VudC11dWlkOjEyMTBmNGFkLTdmYzAtNDZmMC05M2FhLWVmM2NjOWQ3Y2RkMCIsImNsaWVudC1jaXR5OtCf0YHQutC-0LIsINCf0YHQutC-0LLRgdC60LDRjyDQvtCx0LsuIiwic29saWQtYWRkcmVzczpmYWxzZSIsImZ1bGwtbmFtZTrQm9GL0LrQvtCyINCS0Y_Rh9C10YHQu9Cw0LIg0JDQvdCw0YLQvtC70YzQtdCy0LjRhywg0JjQvdC00LjQstC40LTRg9Cw0LvRjNC90YvQuSDQv9GA0LXQtNC_0YDQuNC90LjQvNCw0YLQtdC70YwiLCJjbGllbnQtaWQtZWM0OjMxOTE2NDEiXSwianRpIjoiYWMyZDQ2YjktM2I2MS00ZWRmLWEyMmQtOTBiZWVhMDk5MDA4IiwiY2xpZW50X2lkIjoiUzYxbldlQnlIWWFPOVo5cVlOc0FJejRMVkR2WHlsVWEifQ.OHKLfFM0dUx0L2ZnKlv4zNCFl1aZ5C4Q2kCeO-YyHFLAbJE6lR6eBLCnji5_BMNuDluAetH82Nf7CX7hsjuzD7T5acDXGDTtyb02LKPL_FzUcwnhFLsPVpUROgvCQQ1HQZrhQqrX84ZRDCG1YCbMMpRRLwqGk_d4pMIwfMheqrPgpHEOX4l4XsBJr_TgTF_8pRspPZTTBoYLSK4pZOLimn2kWJr9UxwFj1UyXgLxdTGT_ejR4iqHZOvcle0NnV_P3FjgSvwPAsKrSLwgHayUJK-NPyqN3LsPCJx27i-iIGXeFYhG5t2wgghjWH1mYka3kqJllMNKU42CV_G0QApIUw',
    #     "expires_in": None
    # }
}


class AuthView:
    """ Получение или запрос токенов сервисов доставки"""

    def get_cdek_token(action=None):
        """ Запрос или возврат токенов CDEK """
        # now_datetime = datetime.datetime.now()
        grant_type = 'client_credentials'
        
        try:
            if action == 'get':
                raise KeyError

            return tokens['cdek']

        except KeyError:
            print('\t!!!ВНИМАНИЕ: ЗАПРОС ТОКЕНА')
            keys = DeleviryServiceModel.objects.get(name="cdek")
            url = f"https://api.cdek.ru/v2/oauth/token/?grant_type={ grant_type }&client_id={ keys.account }&client_secret={ keys.secure }"
            response = requests.post(url)
            if response.status_code == 200:
                r = response.json()
                tokens['cdek'] = {
                    "token": str('Bearer ' + r['access_token']),
                    "expires_in": None
                }
                return tokens['cdek']

            else:
                pass


class CdekRegionView(APIView):
    """ Список доступных регионов """

    def get(self, request):
        try:
            with open('orders/json/cdek_regions.json') as file:
                data = json.load(file)

            return Response(data)

        except FileNotFoundError:
            cdek = AuthView.get_cdek_token()
            url = f'https://api.cdek.ru/v2/location/regions?country_codes=RU'
            headers = {
                "Authorization": cdek["token"]
            }

            response = requests.request("GET", url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                # Сохраняем данные, для экономии запросов к API
                with open('orders/json/cdek_regions.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False)

                return Response(data)
            else:
                print('Не получили регионы', response)
                AuthView.get_cdek_token('get')
                return Response(status=status.HTTP_200_OK)


class CdekCityView(APIView):
    """ Список доступных городов """

    def get(self, request, region_code):

        try:
            with open(f'orders/json/cdek_city_{ region_code }.json') as file:
                data = json.load(file)

            return Response(data)
        
        except FileNotFoundError:
            cdek = AuthView.get_cdek_token()

            url = f'https://api.cdek.ru/v2/location/cities/?region_code={ region_code }'
            headers = {
                "Authorization": cdek["token"]
            }

            response = requests.request("GET", url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                # Сохраняем данные, для экономии запросов
                with open(f'orders/json/cdek_city_{ region_code }.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False)

                return Response(data)
            else:
                AuthView.get_cdek_token(action='get')
                return Response(status=status.HTTP_400_BAD_REQUEST)


class TariffListView(APIView):
    """ 
    Калькулятор. Расчет по доступным тарифам 
    Уточнять все точки старта
    """
    shop_code = {
        "PSK": 393,
        "MOW":  44,
        "SPE": 137,
        "SMO": 395,
        "KR" : 450,
        "PSK1": 1315,
    }
    url = "https://api.cdek.ru/v2/calculator/tarifflist"

    def post(self, request):
        cdek = AuthView.get_cdek_token()

        data = request.data
        start_point = data['startpoint']
        end_point = data['endpoint']

        delivery_response = None
        counter = 0

        for product in data['products']:
            counter += 1
            weight, length, width, height = None, None, None, None

            print(product['propstrmodel'])

            #Находим параметры товара
            try:
                for param in product['propstrmodel']:
                    if param['qname'] == '7z26':
                        weight = int(param['value'].replace(',', '') + '000')

                    if param['qname'] in ['kbsp', '3b0e']:
                        size = param['value'].replace(" ", "")
                        length, width, height = int(size[0:2]) + 1, int(size[4:6]) + 1, int(size[8:10]) + 1
            except TypeError: 
                return Response({"error": "Невозможно расчитать стоимость доставки" })


            if weight and length and width and height:

                headers = {
                    'Authorization': cdek['token'],
                    'Content-Type': 'application/json'
                    }

                payload = json.dumps({
                    "type": 1,
                    "date": None,
                    "currency": 1,
                    "lang": "rus",
                    "from_location": {
                        "code": self.shop_code[start_point['region_code']]
                    },
                    "to_location": {
                        "code": end_point['city_code']
                    },
                    "packages": [
                        {
                        "height": height,
                        "length": length,
                        "weight": weight,
                        "width": width
                        }
                    ]
                    })

                response = requests.request("POST", self.url, headers=headers, data=payload)

                # Имеет проблему с устаревшим токеном
                if response.status_code == 200:
                    tarifs = response.json()['tariff_codes']
                else:
                    print(response.status_code)
                    AuthView.get_cdek_token('get')
                    return Response({"error": "RESPONSE NOT 200" })

            else:
                return Response({"error": "Невозможно расчитать стоимость доставки" })


            # Поправка расчётов исходя из кол-ва позиций !!! 
            try:
                if product['quantity'] > 1:
                    for tarif in tarifs:
                        tarif['delivery_sum'] = tarif['delivery_sum'] * product['quantity']
            except KeyError:
                pass


            # Наложение доставки товаров
            if delivery_response:
                for update_data in tarifs:
                    for data in delivery_response:
                        if data['tariff_code'] == update_data['tariff_code']:
                            data['delivery_sum'] = data['delivery_sum'] + update_data['delivery_sum']

            else:
                delivery_response = tarifs


        return Response({'tariff_codes': delivery_response })


# class TestView(APIView):
#     """ Тестируем идеи """

#     def get(self, response):

#         data_1 = [{'tariff_code': 480, 'tariff_name': 'Экспресс дверь-дверь', 'tariff_description': 'Экспресс-доставка', 'delivery_mode': 1, 'delivery_sum': 5000.0, 'period_min': 4, 'period_max': 5, 'calendar_min': 5, 'calendar_max': 6}, {'tariff_code': 482, 'tariff_name': 'Экспресс склад-дверь', 'tariff_description': 'Экспресс-доставка', 'delivery_mode': 3, 'delivery_sum': 5200.0, 'period_min': 4, 'period_max': 5, 'calendar_min': 5, 'calendar_max': 6}]
#         data_2 = [{'tariff_code': 480, 'tariff_name': 'Экспресс дверь-дверь', 'tariff_description': 'Экспресс-доставка', 'delivery_mode': 1, 'delivery_sum': 6000.0, 'period_min': 4, 'period_max': 5, 'calendar_min': 5, 'calendar_max': 6}, {'tariff_code': 482, 'tariff_name': 'Экспресс склад-дверь', 'tariff_description': 'Экспресс-доставка', 'delivery_mode': 3, 'delivery_sum': 6200.0, 'period_min': 4, 'period_max': 5, 'calendar_min': 5, 'calendar_max': 6}]



#         for a in data_1:
#             print('ADD: ', a['delivery_sum'])

#             for b in data_2:
#                 if b['tariff_code'] == a['tariff_code']:
#                     b['delivery_sum'] = b['delivery_sum'] + a['delivery_sum']

#                     print('CALC: ', b['delivery_sum'])


#             print(a)

#         print('\nRETURN DATA:\t', data_2)

#         return Response(a)


#     def post(self, response):

#         print(response.data)

#         return Response({"success": "Пользователь подписан"})
#         # return Response({"exist": "Пользователь существует"})

#         # return Response(status=status.HTTP_400_BAD_REQUEST)