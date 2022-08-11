from rest_framework import serializers
from forum.models import *


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryModel
        fields = ('id', 'name', 'description',)


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopicModel
        fields = ('id', 'created_date', 'username', 'title', 'description',)


class PostsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostModel
        fields = '__all__'

