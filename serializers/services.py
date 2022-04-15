from rest_framework import serializers
from catalog.models import PriceModel, ShopAdressModel, AvailableModel, ProductModel


class PriceSerializer(serializers.Serializer):
    """Сериализатор цен для 1С"""

    shop_UID = serializers.CharField(max_length=100)
    prod_UID = serializers.CharField(max_length=100)
    price = serializers.FloatField()
    currency = serializers.CharField(max_length=4)



class AvailableSerializer(serializers.Serializer):
    """Сериализатор наличия"""

    shop_UID = serializers.CharField(max_length=100)
    prod_UID = serializers.CharField(max_length=100)
    status = serializers.CharField(max_length=100)
    quantity = serializers.IntegerField()


class ProdsServiceSerializer(serializers.Serializer):
    """ Общий сериализатор цен и наличия """

    shop_UID = serializers.CharField(max_length=100,)
    prod_UID = serializers.CharField(max_length=100,)
    price = serializers.FloatField() 
    currency = serializers.CharField(max_length=5, allow_blank=True)
    quantity = serializers.FloatField()