from rest_framework import serializers
from dreamkas.models import DreamkasProductModel, ReceiptsStatusModel


class DreamkasProductSerializer(serializers.ModelSerializer):
    """ Сериализатор товаров """

    class Meta:
        model = DreamkasProductModel
        fields = (
            'id',
            'name',
            'type',
            'quantity',
            # 'createdAt',
            # 'updatedAt',
            'tax',
            'isMarked',
        )


class ReceiptsStatusSerializer(serializers.ModelSerializer):
    """ Сериализатор товаров """

    class Meta:
        model = ReceiptsStatusModel
        fields = ('id', 'externalId', 'createdAt', 'status',)