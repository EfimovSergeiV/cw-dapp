from rest_framework import serializers
from content.models import *


class WideBannersSerializer(serializers.ModelSerializer):
    """ Сериализатор широких баннеров """

    class Meta:
        model = WideBannersModel
        fields = ('id', 'name', 'image', 'link', 'path', ) 


class VotesAnswersSerializer(serializers.ModelSerializer):
    """ Сериализатор для ответов на вопросы """

    class Meta:
        model = VotesAnswersModel
        fields = ('id', 'answer', 'voted',)


class VotesSerializer(serializers.ModelSerializer):
    """ Сериализатор для опросов """

    answers = VotesAnswersSerializer(many=True, read_only=True)
    
    class Meta:
        model = VotesModel
        fields = ('id', 'vote', 'answers')

class ReviewsSerializer(serializers.ModelSerializer):
    """ Сериализатор видео обзоров на оборудование """

    class Meta:
        model = ReviewsModel
        fields = ('id', 'name', 'link', 'video', 'image', 'show_image', 'static_image')


class ArticleSerializer(serializers.ModelSerializer):
    """ Сериализатор статей """

    class Meta:
        model = ArticleModel
        fields = ('id', 'title', 'text',)