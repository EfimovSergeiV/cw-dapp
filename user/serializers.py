from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from user.models import *
from serializers.catalog import ProductSerializer


class LikesProductsSR(serializers.ModelSerializer):
    """ Понравившиеся товары """

    class Meta:
        model = LikeProdModel
        fields = '__all__'


class SubscriberSerializer(serializers.ModelSerializer):
    """ Подписчики """

    class Meta:
        model = SubscriberModel
        fields = '__all__'
        

class LikeProductDetailSR(LikesProductsSR):
    """ Понравившиеся товары с информацией о товаре """

    product = ProductSerializer()


class MainProductReviewSR(serializers.ModelSerializer):
    """ Лень писать created , позже мб"""

    class Meta:
        model = ProductReviewModel
        fields = ('id', 'user', 'product', 'date', 'grade', 'review',)


class ProductReviewSR(MainProductReviewSR):
    """ Сериализатор отзывов на товар"""
    # user = serializers.CharField(source='user.username', read_only=True)
    pass


class FeedBackSerializer(serializers.ModelSerializer):
    """ Обратная связь с общей формы сообщений """

    class Meta:
        model = FeedBackModel
        fields = '__all__'


class UserWatcherUUIDSerializer(serializers.ModelSerializer):
    """  """

    class Meta:
        model = UserWatcherModel
        fields = '__all__'


from catalog.serializers import ProductSerializer
class UserWatcherSerializer(serializers.Serializer):
    """ Отслеживаемые пользователем товары """
   
    viewed = ProductSerializer(many=True)
    like = ProductSerializer(many=True)
    comp = ProductSerializer(many=True)



class DataUserOrdersSerializer(serializers.Serializer):
    """ История заказов пользователя """

    userdata = serializers.JSONField()


class GoogleUserSerializer(serializers.ModelSerializer):
    """ Пользователи авторизованные через Google """

    class Meta:
        model = GoogleUserModel
        fields = '__all__'