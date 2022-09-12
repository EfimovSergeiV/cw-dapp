# Определение местоположения пользователя по ip адресу
# pip install geoip2
# mkdir geoip-db
# Upload database 'GeoLite2 City' from (https://www.maxmind.com/en/accounts/639907/geoip/downloads) to geoip-db dir

import json
from django.contrib.auth.models import User
from django.http import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from serializers.main import *
from django.http import HttpResponse
from main.verification import *
from main.models import UserIdentificationServiceModel
from ipware import get_client_ip
from django.core.mail import send_mail
import requests
import random
from main.settings import BASE_DIR
from django.template.loader import render_to_string
from django.shortcuts import render

import geoip2.database


def send_err(err, message):
    """ Отправка ошибок на sys@tehnosvar.ru """
    send_mail(
        err,
        message,
        'shop@glsvar.ru',
        ['sys@tehnosvar.ru'],
        fail_silently=False,
    )


class VersionControlView(APIView):
    """ Актуальная версия клиента """
    serializer_class = VersionControlSerializer

    def get(self, request):
        qs = VersionControlModel.objects.latest('id')
        serializer = self.serializer_class(qs)
        return Response(serializer.data)


class MainPageView(APIView):
    """
    Главная страница API
    Написать сюда документацию к API,
    приглашение в админку и форму саппорта
    """
    def get(self, request):
        html = "<html><body><h1>API GLSVAR ver 2.0</h1></body></html>"
        return HttpResponse(html)



class AuthTokenView(ObtainAuthToken):
    """Отдаём токен и информацию о пользователе"""
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'userid': user.pk,
            'user': user.username,
            'email': user.email,
            })


class SignUpView(APIView):
    """ Стандартная регистрация пользователей """
    
    def post(self, request, format=None):
        serializer_user = UserSerializer(data=request.data)
        
        check_email = User.objects.filter(email=request.data['email']).exists()

        if serializer_user.is_valid() and not check_email:
            user = User.objects.create(
                username= serializer_user.initial_data['username'],
                first_name = serializer_user.initial_data['first_name'],
                last_name = serializer_user.initial_data['last_name'],
                email= serializer_user.initial_data['email'],
            )
            user.set_password(serializer_user.initial_data['password'])
            user.save()
            # mail_list = [
            #     serializer_user.data['email'],
            #     ]
            # SugnUpMails.send_notice(email=mail_list, data=serializer_user.data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SubscriebeUserView(APIView):
    """ Быстрая регистрация пользователей """
    
    def post(self, request):        
        try:
            email = request.data["email"]
            check_email = User.objects.filter(email=email).exists()

            if check_email:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            else:
                gen_pass = random.randrange(00000000, 19999999)
                html_content = render_to_string('subscriebe.html', {'gen_pass': gen_pass})
                
                serializer = UserSerializer(
                    data = { "username": email, "email": email, "password": gen_pass }
                )

                if serializer.is_valid():
                    user = User.objects.create(
                        username= serializer.data['username'],
                        email= serializer.data['email'],
                    )
                    user.set_password(serializer.data['password'])
                    user.save()

                    send_mail(
                        'Благодарим за регистрацию на нашем сайте',
                        message=html_content,
                        from_email= 'shop@glsvar.ru',
                        recipient_list= [email],
                        fail_silently=False,
                        html_message=html_content
                        )
                    print("Создан новый пользователь")
                else:
                    print("Serializer not valid")


                
                return Response(status=status.HTTP_201_CREATED)

        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangeUserView(APIView):
    """ Изменить информацию о пользователе """

    pass

    # permission_classes = [IsAuthenticated,]

    # def post(self, request):
    #     user = request.user.username
    #     print(user)
        
    #     return Response(status=status.HTTP_201_CREATED)


class RestoreUserPassword(APIView):
    """ Восстановить пароль пользователя """

    def post(self, request):
        """
        TASK: Добавить предварительное уведомление перед сменой пароля
        пользователю
        """
        try:
            email = request.data["email"]
            check_email = User.objects.filter(email=email).exists()
            if check_email:
                gen_pass = random.randrange(00000000, 19999999)    

                try:
                    user = User.objects.get(email=email)
                    user.set_password(str(gen_pass))
                    user.save()
                    html_content = render_to_string('restore-pass.html', {'gen_pass': gen_pass})
                    send_mail(
                        'Сброс пароля пользователя',
                        message=html_content,
                        from_email= 'shop@glsvar.ru',
                        recipient_list= [email],
                        fail_silently=False,
                        html_message=html_content
                        )
                
                except:
                    pass

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)   #({ "error": 'UserNotFound'})

            return Response(status=status.HTTP_200_OK)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """ Информация о пользователе """

    permission_classes = [IsAuthenticated,]

    def get(self, request):
        user = request.user
        profile = User.objects.get(username=user)

        try:
            prof_custom = ProfileModel.objects.get(user=user)
        except:
            prof_custom = { "phone": None, "adress": None}

        username = profile.username if profile.username else 'не указано'
        first_name = profile.first_name if profile.first_name else 'не указано'
        last_name = profile.last_name if profile.last_name else 'не указано'
        email = profile.email if profile.email else 'не указано'

        try:
            phone = prof_custom.phone if prof_custom.phone else 'не указано'
            adress = prof_custom.adress if prof_custom.adress else 'не указано'
        except:
            phone = 'не указано'
            adress = 'не указано'


        return Response(
            {
                "username" : username,
                "first_name" : first_name,
                "last_name" : last_name,
                "email" : email,
                "phone" : phone,
                "adress" : adress,
            }
        )
    
    def post(self, request):
        resp = { "msg": "Данные сохранены", "variant": "success" }
        user = request.user

        user_data = {}
        prof_data = {}

        for item in request.data:
            if item in ['phone', 'adress',]:
                if request.data[item] != None and len(request.data[item]) > 3:
                    prof_data[item] = request.data[item]
            if item in ['username', 'first_name', 'last_name', 'email']:
                if request.data[item] != None and len(request.data[item]) > 3:
                    user_data[item] = request.data[item]

        try:
            # Update user profile
            ProfileModel.objects.get(user=user)
            ProfileModel.objects.filter(user=user).update(**prof_data)

        except ProfileModel.DoesNotExist:
            # Create user profile
            ProfileModel.objects.create(user=user, **prof_data)

        User.objects.filter(username=user).update(**user_data)


        # print(
        #     'UserData: ', user_data, '\n',
        #     'ProfData: ', prof_data,
        #     )

        try:
            password = request.data["password"]
            if len(password) == 0:
                pass
            elif 20 > len(password) > 8:
                user = User.objects.get(username=user.username)
                user.set_password(password)
                user.save()
            else:
                resp = { "msg": "Слишком короткий пароль", "variant": "danger" }
        except KeyError:
            pass

        return Response(resp)


class ReturnClientLocation(APIView):
    """ Определение местоположения пользователя по IP """

    def get(self, request):
        """ 
        Возвращаем только успешные местоположения,
        исходя из того что по региону есть магазин.
        В противном случае возвращаем Москву.
        Игнорируем запросы, со своего IP.
        """

        client_ip = get_client_ip(request)[0]


        try:
            # Отсеиваем свои IP и минимизируем запросы в сервис
            if client_ip in ['127.0.0.1', '91.204.138.138']:
                with open( str(BASE_DIR / 'main/location/pskov_location.json'), 'r') as file:
                    location = json.load(file) # Если IP из списка, возвращаем Псков

            else:
                service = UserIdentificationServiceModel.objects.filter(activated=True)
                use_service = service[0]
                url_service = use_service.service_url + client_ip + '?access_key=' + use_service.service_key
                response = requests.get(url_service)

                # Возвращаем Москву, если нет магазина по местоположению пользователя
                if response.json()['region_code'] in [
                                                # "182100", # Великие луки
                                                "PSK", # Псков
                                                "MOW", # Москва
                                                "SPE", # Санкт-Петербург
                                                "KR", # Петрозаводск
                                                "SMO", # Смоленск
                                                ]:

                    location = response.json()

                else:
                    with open( str(BASE_DIR / 'main/location/moscow_location.json'), 'r') as file:
                        location = json.load(file) # Если всё плохо, возвращаем Москву
        except Exception as err:
            
            with open(str(BASE_DIR / 'logs/location_err.log'), 'w') as err_file:
                err_file.write(str(err) + '\n' + str(response.json()) + '\n' + str(url_service))
            
            with open( str(BASE_DIR / 'main/location/pskov_location.json'), 'r') as file:
                location = json.load(file) # Если всё плохо, возвращаем Москву

        return Response(location)


class NearShop(APIView):
    """ Определение ближайшего магазина к пользователю """
    # pip install geoip2
    # mkdir geoip-db
    # Upload database 'GeoLite2 City' from (https://www.maxmind.com/en/accounts/639907/geoip/downloads) to geoip-db dir
    # PR: Прописать модель и админку для обновления базы 'GeoLite2 City'

    shops = {
        'Москва': {
            "shop": {
                "shop_id": 9,
                "region_code": 'MOW',
                "city": 'Москва',
                "adress": 'Москва, ул Николая Химушина д 2/7 с 38',
                "phones": [
                    { "number": '+7 (495) 970-30-43', "link": '+74959703043' },
                    { "number": '+7 (495) 970-40-63', "link": '+74959704063' },
                ],
                'mapurl':
                    'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1294.9674262543072!2d37.75825094281362!3d55.81609851189722!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46b5351d0a30f399%3A0x35126e53033abe8c!2z0JPQu9Cw0LLQvdGL0Lkg0YHQstCw0YDRidC40Lo!5e0!3m2!1sru!2sru!4v1644216636444!5m2!1sru!2sru',
            },
        },

        'Санкт-Петербург': {
            "shop": {
                "shop_id": 1,
                "region_code": 'SPE',
                "city": 'Санкт-Петербург',
                "adress": 'Санкт-Петербург, шоссе Революции, д.84, литера Е',
                "phones": [
                    { "number": '+7 (812) 336-93-81', "link": '+78123369381' },
                    { "number": '+7 (812) 703-50-13', "link": '+78127035013' },
                ],
                'mapurl':
                    'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1997.2501459329694!2d30.452679000000003!3d59.961174!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46963212079136a5%3A0x539eb2bc6ec0bd89!2z0JPQu9Cw0LLQvdGL0Lkg0YHQstCw0YDRidC40Lo!5e0!3m2!1sru!2sru!4v1644216895501!5m2!1sru!2sru',

            },
        },

        'Псков': {
            "shop": {
                "shop_id": 6,
                "region_code": 'PSK',
                "city": 'Псков',
                "adress":
                'Псков, ул.Леона Поземского, 92, Павильон 28 (рынок на Алмазной)',
                "phones": [
                    { "number": '+7 (8112) 70-10-80', "link": '+78112701080' },
                ],
                'mapurl':
                    'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2124.198942962845!2d28.310578951637158!3d57.831909281067674!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46c01ebf22b5141b%3A0x70646a1ae845f205!2z0JPQu9Cw0LLQvdGL0Lkg0YHQstCw0YDRidC40Lo!5e0!3m2!1sru!2sru!4v1644217067475!5m2!1sru!2sru',

            },
        },

        'Смоленск': { 
            "shop": {
                "shop_id": 4,
                "region_code": 'SMO',
                "city": 'Смоленск',
                "adress":
                'Смоленск, ул. Посёлок Тихвинка 69, ТК "Город Мастеров" павильон №21',
                "phones": [
                    { "number": '+7 (4812) 67-33-22', "link": '+74812673322' },
                ],
                'mapurl':
                    'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2303.1242853675417!2d32.08359595152002!3d54.7426169801986!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46ce58ed516ce31d%3A0x19590ae134c0098b!2z0KHQv9C10YbQuNCw0LvQuNC30LjRgNC-0LLQsNC90L3Ri9C5INC80LDQs9Cw0LfQuNC9ICLQk9C70LDQstC90YvQuSDQodCy0LDRgNGJ0LjQuiI!5e0!3m2!1sru!2sru!4v1644217468162!5m2!1sru!2sru',
            },
        },
        'Петрозаводск': {
            "shop": {
                "shop_id": 2,
                "region_code": 'KR',
                "city": 'Петрозаводск',
                "adress": 'Петрозаводск, ул. Заводская, д. 2',
                "phones": [
                    { "number": '+7 (8142) 33-12-23', "link": '+78142331223' },
                ],
                'mapurl':
                    'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1884.4024580276966!2d34.30823665179406!3d61.81611808251161!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46a1eea4d25036f7%3A0xa85b3986983b8d00!2z0JPQu9Cw0LLQvdGL0Lkg0KHQstCw0YDRidC40Los!5e0!3m2!1sru!2sru!4v1644218055546!5m2!1sru!2sru',
            },
        },
        'Великие Луки': {
            "shop": {
                "shop_id": 5,
                "region_code": 'PSK1',
                "city": 'Великие Луки',
                "adress": 'Великие Луки, проспект Ленина д.57',
                "phones": [
                    { "number": '+7 (81153) 56-575', "link": '+78115356575' },
                ],
                'mapurl':
                    'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2211.471690236029!2d30.53352345158005!3d56.33894568061954!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46c68c61a3bf1d85%3A0x303d5bb69f3a8816!2z0JzQsNCz0LDQt9C40L0g4oCc0JPQu9Cw0LLQvdGL0Lkg0KHQstCw0YDRidC40LrigJ0sINGB0LLQsNGA0L7Rh9C90L7QtSDQvtCx0L7RgNGD0LTQvtCy0LDQvdC40LUg0Lgg0LzQsNGC0LXRgNC40LDQu9GL!5e0!3m2!1sru!2sru!4v1644218146313!5m2!1sru!2sru',
            },
        }
    }

    def get(self, request):
        client_ip = get_client_ip(request)[0]

        if client_ip not in ['127.0.0.1', '91.204.138.138']:
            try:
                # This reader object should be reused across lookups as creation of it is
                # expensive.
                with geoip2.database.Reader('main/geoip-db/GeoLite2-City.mmdb') as reader:
                    response = reader.city(client_ip)
                    # response = reader.city('195.218.132.1') # Проверка
                    try:
                        city = response.city.names['ru']
                        if city in [
                            'Москва',           #195.218.132.1
                            'Санкт-Петербург',  #5.101.152.110
                            'Псков',            #91.204.138.138
                            'Смоленск',         #88.135.63.198
                            'Петрозаводск',     #178.19.251.89
                            'Великие Луки',     #109.238.108.40
                            ]:
                            location = self.shops[city]
                        else:
                            location = self.shops['Санкт-Петербург']
                    except:
                        location = self.shops['Санкт-Петербург']
            except FileNotFoundError:
                location = self.shops['Санкт-Петербург']

        else:
            location = self.shops['Псков']

        # print(f"RETURN REQUEST: {location}")
        return Response(location)


class ClientIpAdressView(APIView):
    """ Return client IP adress """

    def get(self, request):
        client_ip = get_client_ip(request)[0]
        # For testing
        if client_ip == '127.0.0.1':
            client_ip = '91.204.138.138'
            
        return Response(client_ip)



    

from django import forms


class NameForm(forms.Form):
    name = forms.CharField(label='Имя Фамилия', max_length=100)
    job = forms.CharField(label='Должность', max_length=100)
    worker = forms.CharField(label='Рабочий телефон', max_length=40)
    private = forms.CharField(label='Мобильный телефон', max_length=40)



def signature_generator(request):
    """ Генератор электронных подписей для сотрудников """
    
    if request.method == 'POST':
        form = NameForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            worker_link = data['worker'].replace("+", "").replace(" ", "").replace("(", "").replace(")", "")[0: 11]
            private_link = data['private'].replace("+", "").replace(" ", "").replace("(", "").replace(")", "")[0: 11]

            return render(request, 'sb.html', {
                    'name': data['name'],
                    'job': data['job'],
                    'worker': data['worker'],
                    'private': data['private'],
                    'worker_link': worker_link,
                    'private_link': private_link, 
                })

    else:
        form = NameForm()


    return render(request, 'sb-generator.html', {})