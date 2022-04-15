from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status
import time

from serializers.content import *
from content.models import *


#Header banners
class MainBannerView(APIView):
    """ Карусель на главной странице """

    def get(self, request):
        banners = MainBannerModel.objects.filter(activated=True)
        serializer = MainBannerSerializer(banners, many=True, context={'request':request})
        return Response(serializer.data)


# class SecondBannerView(APIView):
#     """ Второстепенные банеры на главной странице """

#     def get(self, request):
#         sbanners = SecondBannerModel.objects.filter(activated=True)
#         serializer = SecondBannerSerializer(sbanners, many=True)
#         return Response(serializer.data)


#Promo Banners
class MainPromoBannerView(APIView):
    """  """

    def get(self, request):
        sbanners = MainPromoBannerModel.objects.filter(activated=True)
        serializer = MainPromoBannerSerializer(sbanners, many=True, context={'request':request})
        return Response(serializer.data)

# class SecondPromoBannerView(APIView):
#     """  """

#     def get(self, request):
#         sbanners = SecondPromoBannerModel.objects.filter(activated=True)
#         serializer = SecondPromoBannerSerializer(sbanners, many=True)
#         return Response(serializer.data)



# class CityView(APIView):
#     """ Города """

#     def get(self, request):
#         city = CityModel.objects.all()
#         serializer = CitySerializer(city, many=True)
#         return Response(serializer.data)


class FooterFileView(APIView):
    """ Общие сертификаты и документы """

    def get(self, request):
        file_name = FooterFileModel.objects.all()
        serializer = FooterFileSerializer(file_name, many=True, context={'request':request})
        return Response(serializer.data)