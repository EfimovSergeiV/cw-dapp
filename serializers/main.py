from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from main.models import VersionControlModel
from user.models import *


class UserSerializer(serializers.ModelSerializer):
    """ Пользователи сайта """

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')


class VersionControlSerializer(serializers.ModelSerializer):
    """ Контроль версий приложения """

    class Meta:
        model = VersionControlModel
        fields = ('version',)