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
        serializer = VotesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FooterFileView(APIView):
    """ Общие сертификаты и документы """

    def get(self, request):
        file_name = FooterFileModel.objects.all()
        serializer = FooterFileSerializer(file_name, many=True, context={'request':request})
        return Response(serializer.data)