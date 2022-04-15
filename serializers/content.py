from rest_framework import serializers
from content.models import *


class MainBannerSerializer(serializers.ModelSerializer):
    """ Главный баннер на HOME PAGE"""

    class Meta:
        model = MainBannerModel
        fields = ('id', 'name', 'link', 'outlink', 'image', 'description')


class MainPromoBannerSerializer(serializers.ModelSerializer):
    """ Main Promo Banners """

    class Meta:
        model = MainPromoBannerModel
        fields = (
            'id', 
            'name', 
            'tposition', 
            'file_pdf', 
            'link',
            'image',
            'description',
            'dposition',
            )


class FooterFileSerializer(serializers.ModelSerializer):
    """ Общие сертификаты и лицензии """

    class Meta:
        model = FooterFileModel
        fields = ('id', 'name', 'description', 'file_name')