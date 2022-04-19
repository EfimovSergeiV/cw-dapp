from rest_framework import serializers
from dreamkas.models import DreamkasProductModel, ReceiptsStatusModel


# class DreamkasPriceSerializer(serializers.ModelSerializer):
#     """ Серииализатор товаров """

#     class Meta:
#         model = DreamkasPriceModel
#         fields = ('deviceId', 'value',)


class DreamkasProductSerializer(serializers.ModelSerializer):
    """ Сериализатор товаров """

    # prices = DreamkasPriceSerializer(many=True)

    class Meta:
        model = DreamkasProductModel
        fields = (
            'id',
            'name',
            'type',
            'quantity',
            # 'createdAt',
            # 'updatedAt',
            'price',
            'tax',
            'isMarked',
            'prices',
        )


class ReceiptsStatusSerializer(serializers.ModelSerializer):
    """ Сериализатор товаров """

    class Meta:
        model = ReceiptsStatusModel
        fields = ('id', 'externalId', 'createdAt', 'status',)