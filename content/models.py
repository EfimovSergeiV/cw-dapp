from os import name
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH
from main.models import *


class MainBannerModel(AbsActivatedModel):
    """Модель баннеров на главной странице"""
    name = models.CharField(verbose_name="Название", default="ГлавныйСварщик", max_length=100)
    link = models.JSONField(verbose_name="Внутренняя ссылка", max_length=100, null=True, blank=True, help_text="""Пример: {"name": "products", "query": {"brnd": 9, "page": 1}}""")
    outlink = models.URLField(verbose_name="Внешняя ссылка", null=True, blank=True, help_text="Пример: https://outlink.ru/files/file.pdf")
    image = models.ImageField(
        verbose_name="Изображение баннера", 
        help_text="Разрешение: 960X540", 
        upload_to="img/c/banner/")
    description = models.TextField(verbose_name="Описание", max_length=100, default="Интернет магазин сварочного оборудования и расходных материалов")

    class Meta:
        ordering = ['-id', ]
        verbose_name = "Главный баннер"
        verbose_name_plural = "Главные баннеры"

    def __str__(self):
        return str(self.name)


class MainPromoBannerModel(AbsActivatedModel):
    TPN = (
        ('bottomleft', 'Внизу слева'),
        ('topleft', 'Сверху слева'),
        ('topright', 'Сверху справа'),
        ('bottomright', 'Внизу справа'),
        ('centered', 'По центру'),
    )
    name = models.CharField(verbose_name="Название", default="изображение", max_length=100)
    tposition = models.CharField(verbose_name="Место",  choices=TPN, default='topright', max_length=60)
    file_pdf = models.FileField(verbose_name="PDF файл", upload_to='pdf/c/promo/', null=True, blank=True)
    link = models.JSONField(verbose_name="Ссылка URL", max_length=100, default=None , null=True, blank=True,
        help_text = 
        """
        Пример: \n
        { "name": "success", "query": { "ct": 8, "page":2 } }
        Документация: https://api.glsvar.ru/docs.json
        """
        )
    image = models.ImageField(
        verbose_name="Изображение", 
        help_text="Проверенное разрешение изображения 1110Х380PX.", 
        upload_to="img/c/promo/")
    description = models.TextField(verbose_name="Описание", max_length=100, null=True, blank=True)
    dposition = models.CharField(verbose_name="Место",  choices=TPN, default='bottomleft', max_length=60)

    class Meta:
        verbose_name = "PROMO баннер"
        verbose_name_plural = "PROMO баннеры"
        ordering = ['-id',]

    def __str__(self):
        return str(self.name)


# Сертификаты ГС
class FooterFileModel(models.Model):
    """ Файлы """
    name = models.CharField(verbose_name="Название", max_length=100)
    description = models.TextField(verbose_name="Описание", max_length=2000)
    file_name = models.FileField(verbose_name="Файл", help_text="Будет находиться внизу сайта", upload_to="img/c/files/")

    class Meta:
        verbose_name = "Сертификат GS"
        verbose_name_plural = "Сертификаты GS" 

    def __str__(self):
        return self.name