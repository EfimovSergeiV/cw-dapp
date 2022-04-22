from django.db.models import fields
from rest_framework import serializers
from orders.models import *


class OneSotfOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedProductModel
        fields = '__all__'


class OneSoftOrderSerializer(serializers.ModelSerializer):
    client_product = OneSotfOrderSerializer(many=True)
    class Meta:
        model = CustomerModel
        fields = (
            'order_number',
            'total',
            'date_created',
            'status',
            'client_product',
        )


class OrderProductSerializer(serializers.ModelSerializer):
    """ Серииализатор заказанных товаров клиента """

    class Meta:
        model = OrderedProductModel
        fields = '__all__'

class OrderListSerializer(serializers.ModelSerializer):
    """ Сериализатор заказов клиента """

    client_product = OrderProductSerializer(many=True)
    class Meta:
        model = CustomerModel
        fields = (
            'order_number',
            'total',
            'date_created',
            'status',
            'client_product',
        )


class QOrderListSerializer(serializers.ModelSerializer):
    """ Сериализатор заказов клиента со всеми полями """

    client_product = OrderProductSerializer(many=True)
    class Meta:
        model = CustomerModel
        fields = '__all__'


class SmOrderListSerializer(serializers.ModelSerializer):
    """ Сериализатор заказов клиента со всеми полями """

    client_product = OrderProductSerializer(many=True)
    class Meta:
        model = CustomerModel
        fields = ("order_number", "status", "position_total", "delivery_summ", "total", "client_product")


class OrderedProductSerializer(serializers.ModelSerializer):
    """ Сериализатор товаров
    !!! Дубль, можно удалить !!!
    """

    class Meta:
        model = OrderedProductModel
        fields = (
            'id',
            'product_id',
            'vcode',
            'name',
            'price',
            'preview_image',
            'quantity',
        )


class CustomerSerializer(serializers.ModelSerializer):
    """ Сериализатор клиента """
    client_product = OrderedProductSerializer(many=True)

    class Meta:
        model = CustomerModel
        fields = (
            'uuid',
            'order_number',
            'adress',
            'position_total',
            'total',
            'delivery',
            'delivery_adress',
            'delivery_summ',
            'person',
            'phone',
            'email',
            'comment',
            'company',
            'legaladress',
            'inn',
            'kpp',
            'okpo',
            'bankname',
            'currentacc',
            'corresponding',
            'bic',
            'client_product'
        )

    def create(self, validated_data):
        client_product_data = validated_data.pop('client_product')
        client = CustomerModel.objects.create(**validated_data)
        for order in client_product_data:
            OrderedProductModel.objects.create(customer = client, **order)
        return client


class RequestPriceSerializer(serializers.ModelSerializer):
    """ Сериализатор запроса на цену """

    class Meta:
        model = RequestPriceModel
        fields = '__all__'


##################################


# class OrderSerializer(serializers.ModelSerializer):
#     """Сериализатор продуктов"""

#     class Meta:
#         model = OrderedGoodsModel
#         fields = (
#             'id',
#             'vcode',
#             'previewImage',
#             'name',
#             'quantity',
#             'price',
#         )


# class ClientSerializer(serializers.ModelSerializer):
#     """ Сериализатор клиента (старый) """
#     client_product = OrderSerializer(many=True)

#     class Meta:
#         model = ClientModel
#         fields = (
#             'id',
#             'order_numer',
#             'person',
#             'legaladress',
#             'inn',
#             'kpp',
#             'okpo',
#             'bankname',
#             'currentacc',
#             'corresponding',
#             'bic',
#             'company',
#             'phone',
#             'email',
#             'adress',
#             'total',
#             'comment',
#             'client_product',
#         )

#     def create(self, validated_data):
#         client_product_data = validated_data.pop('client_product')
#         client = ClientModel.objects.create(**validated_data)
#         for order in client_product_data:
#             OrderedGoodsModel.objects.create(client = client, **order)
#         return client
