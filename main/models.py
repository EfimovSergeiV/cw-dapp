from pyexpat import model
from tabnanny import verbose
from django.db import models
from django.utils import timezone
from rest_framework import authentication


class BearerAuthentication(authentication.TokenAuthentication):
    '''
    Simple token based authentication using utvsapitoken.

    Clients should authenticate by passing the token key in the 'Authorization'
    HTTP header, prepended with the string 'Bearer '.  For example:

    Authorization: Bearer 956e252a-513c-48c5-92dd-bfddc364e812
    '''

    keyword = 'Bearer'


class AbsDateModel(models.Model):
    """Астрактная модель даты"""
    created_date = models.DateField(verbose_name="Дата создания", default=timezone.now)

    class Meta:
        abstract = True


class AbsActivatedModel(models.Model):
    """Модерация"""
    activated = models.BooleanField(default=False, verbose_name="Активирован")

    class Meta:
        abstract = True
        
        
class AbsProductModel(AbsDateModel, AbsActivatedModel):
    vcode = models.CharField(verbose_name="Артикул", max_length=100)    
    name = models.CharField(max_length=250, verbose_name="Название")
    description = models.TextField(max_length=5500, default="Нет описания", help_text="max lenght 5500", null=True, blank=True, verbose_name="Описание")

    class Meta:
        abstract = True


### SITE SETTINGS APP

class UserIdentificationServiceModel(AbsActivatedModel):
    """ Сервисы определения IP """
    service_url = models.URLField('Адрес сервиса', null=True, blank=True)
    service_key = models.CharField("Ключ сервиса", null=True, blank=True, max_length=200)
    service_statistic = models.IntegerField("Счётчик запросов", default=0, null=True, blank=True)

    class Meta:
        verbose_name = "Сервис идентификации пользователя"
        verbose_name_plural = "Сервисы идентификации пользователя"

    def __str__(self):
        return self.service_key


class VersionControlModel(models.Model):
    """ Контроль версий FrontEnd """

    version = models.CharField(verbose_name="Версия приложения", max_length=20, help_text="1.0.0")
    description = models.TextField(verbose_name="Описание изменений", max_length=1500)

    class Meta:
        verbose_name = "Версия приложения"
        verbose_name_plural = "Версии приложения"

    def __str__(self):
        return self.version


class DeleviryServiceModel(models.Model):
    """ Сервисы доставки товаров, ключи для API """

    name = models.CharField(verbose_name="Название", max_length=100)
    account = models.CharField(verbose_name="Идентификатор", max_length=100, null=True, blank=True)
    secure = models.CharField(verbose_name="Секрет/Пароль", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Сервис доставки"
        verbose_name_plural = "Сервисы доставки"

    def __str__(self) -> str:
        return self.name

class CourceCurrency(models.Model):
    """ Курсы валют """

    name = models.CharField(verbose_name="ISO Название", max_length=3)
    cource = models.FloatField(verbose_name="Стоимость", default=0)

    class Meta:
        verbose_name = "Курс валюты"
        verbose_name_plural = "Курс валюты"

    def __str__(self) -> str:
        return self.name