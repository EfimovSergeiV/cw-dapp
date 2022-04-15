from services.logic.prod_update import daemon_data_uploads
from services.logic.processing import start_process
from django.db.models.aggregates import Count
import requests
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from catalog.models import *
from serializers.services import *

import threading

from services.logic.prod_update import *
import json
from main.settings import BASE_DIR
import os


# Генератор
import string
import random

def gen(size=4, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class AcceptDataView(APIView):
    """  """
    permission_classes = [IsAdminUser]

    def post(self, request):
        """Валидация данных""" # except: return Response({"detail": "Ошибка выгрузки"})
        serializer = ProdsServiceSerializer(data=request.data, many=True)
        if serializer.is_valid():
            thread = threading.Thread(target=start_process, args=(serializer.data,))
            thread.start()
            return Response({"detail": "Успешная выгрузка"})
        else:
            return Response({"detail": "Неверные данные"})


class ProdsServiceView(APIView):
    """

    """

    permission_classes = [IsAdminUser]

    def post(self, request):

        serializer = ProdsServiceSerializer(data=request.data, many=True)


        try:
            if serializer.is_valid():

                # Записываем новые данные с присвоением порядкового номера
                # как названия файла
                len_files = len(os.listdir( str(BASE_DIR) + '/uploads'))
                data = serializer.data

                filename = 'uploads/' + str(len_files) + '.json'
                
                with open(filename, 'w', encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False,)

                # Проверяем изменившиеся данные по предыдущей выгрузке,
                later_filename = 'uploads/' + str( len_files - 1 ) + '.json'
                try:
                    with open(later_filename, encoding="utf-8") as later_file:
                        later_data = json.load(later_file)
                except FileNotFoundError:
                    later_data = [{"err": "нет файла данных."}]


                new_data = list()
                for cursor in data:
                    if dict(cursor) not in later_data:
                        new_data.append(dict(cursor))

                statistic = {
                    "Обнаружено записей: ": len(serializer.data),
                    "Обновлённых записей: ": len(new_data),
                    "Последний выгруженый: ": later_filename,
                    "Созданный файл: ": filename,
                }

                # threads = list()
                upload_data = threading.Thread(target=daemon_data_uploads, args=(new_data, statistic))
                # threads.append(upload_data)
                upload_data.start()

                return Response({"detail": {'Обнаружено записей: ': len(serializer.data)}})

            else:
                return Response({"detail": "Неверный формат данных."})

        except:
            return Response({"detail": "Ошибка выгрузки."})

# В.Луки Розница	647af975-60ab-11e2-8971-10bf4871e437
# Псков Алмазная	958632c1-846a-11e5-806e-0021855f216f
# Смоленск Тихвинка	96dd9447-8fcf-11e3-aa79-0c84dcd0233a
# Санкт-Петербург	e37a0bbb-f47f-11e4-aec3-208984863fbe
# Оптовый	6a4a35c3-60aa-11e2-8971-10bf4871e437
# Псков Шоссейная	3445c227-7efc-11e5-be77-24fd52940c70
# Петрозаводск Розница	d5af83ae-68e6-11e5-8261-c48e8f4373aa
# Рязань Яблочкова	9cb1dfc3-7a78-11e6-ae23-00269e8edcfe
# Смоленск Розница	ae56cf28-bd24-11e2-b408-1c6f652af6ec
# Псков Неелово	1d162cd3-886a-11e5-96e1-14dae9ee1802
