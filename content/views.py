from cgi import print_arguments
from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status
import time

from serializers.content import * #PR: Перенести сюда сериализаторы
from content.serializers import *
from content.models import *


class MainBannerView(APIView):
    """ Карусель на главной странице """

    def get(self, request):
        banners = MainBannerModel.objects.filter(activated=True)
        serializer = MainBannerSerializer(banners, many=True, context={'request':request})
        return Response(serializer.data)


class MainPromoBannerView(APIView):
    """ Баннеры промо на главной странице """

    def get(self, request):
        sbanners = MainPromoBannerModel.objects.filter(activated=True)
        serializer = MainPromoBannerSerializer(sbanners, many=True, context={'request':request})
        return Response(serializer.data)


class VotesView(APIView):
    """ Опросы """

    def get(self, request):
        votes = VotesModel.objects.filter(is_active=True)
        serializer = VotesSerializer(votes, many=True, context={'request':request})
        return Response(serializer.data)


    def post(self, request):
        """ Проверяем есть ли в базе данных опрос и не отвечал ли на него пользователь """
        id = 1 # Получить сюда ID запроса
        try:
            vote = VotesModel.objects.get(id=id)

            ip_adress = '91.204.138.147' # Получить сюда IP адрес пользователя

            if { 'ip_adress': ip_adress } not in vote.interviewed.values('ip_adress'):
                vote.interviewed.create(ip_adress=ip_adress)
                vote.answers.filter(id=2).update(voted=+1)
                
                return Response({"created": "Спасибо за Ваш голос"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Ваш голос уже существует"}, status=status.HTTP_400_BAD_REQUEST)

        except VotesModel.DoesNotExist:
            return Response({"error": "Опрос не найден"}, status=status.HTTP_400_BAD_REQUEST)


class FooterFileView(APIView):
    """ Общие сертификаты и документы """

    def get(self, request):
        file_name = FooterFileModel.objects.all()
        serializer = FooterFileSerializer(file_name, many=True, context={'request':request})
        return Response(serializer.data)