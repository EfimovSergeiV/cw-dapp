import uuid
from django.db import models
from django.utils import timezone


# class AuthTokenModel(models.Model):
#     """ Удалить и повыпиливать при обновлении приложения """

#     activated = models.BooleanField(verbose_name="Активирован", default=False)
#     created = models.DateTimeField(verbose_name="Дата создания", default=timezone.now)
#     token = models.UUIDField(verbose_name="Токен сервиса",)

#     class Meta:
#         verbose_name = "Токен"
#         verbose_name_plural = "Токены"

#     def __str__(self) -> str:
#         return str(self.token)


class DreamkasProductModel(models.Model):
    """ Модель товара Dreamkas """

    TAX_VALUES = (
        ("NDS_NO_TAX", "Без НДС"),
        ("NDS_0", "НДС 0%"),
        ("NDS_10", "НДС 10%"),
        ("NDS_20", "НДС 20%"),
        ("NDS_10_CALCULATED", "НДС 10/110%"),
        ("NDS_20_CALCULATED", "НДС 20/120%")
    )

    TYPE_VALUES = (
        ("COUNTABLE", "Штучный"),
        ("SCALABLE", "Мерный"),
        ("ALCOHOL", "Алкогольный"),
        ("CLOTHES", "Одежда"),
        ("SHOES", "Обувь"),
        ("SERVICE", "Услуга"),
        ("TOBACCO", "Табачная продукция"),
        ("MILK", "Молочная продукция"),
    )

    association = models.PositiveIntegerField(verbose_name="Ассоциирован", null=True, blank=True, help_text="Ассоциация с ID товара")

    id = models.UUIDField(verbose_name="UUID", primary_key=True, help_text="Из 1С (скорее всего)")
    name = models.CharField(verbose_name="Название товара", max_length=350)
    type = models.CharField(verbose_name="Тип", choices=TYPE_VALUES, max_length=20, default="COUNTABLE")
    quantity = models.PositiveIntegerField(verbose_name="Единица товара", default=1000, help_text="Пример: 1000")
    # meta = {},
    createdAt = models.DateTimeField(verbose_name="Дата создания", default=timezone.now)
    updatedAt = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    # price = models.PositiveIntegerField(verbose_name="Цена в копейках", help_text="2 последних знака будут копейками")
    tax = models.CharField(verbose_name="Налог", choices=TAX_VALUES, max_length=20, default="NDS_20")
    isMarked = models.BooleanField(verbose_name="Маркерованный товар", default=False)

    class Meta:
        verbose_name = "Товар Dreamkas"
        verbose_name_plural = "Товары Dreamkas"

    def __str__(self) -> str:
        return str(self.name)


# class DreamkasPriceModel(models.Model):
#     """ Цена для каждого устройства """
#     product = models.ForeignKey(DreamkasProductModel, related_name='prices', on_delete=models.CASCADE)
#     deviceId = models.PositiveIntegerField(verbose_name="ID устройства")
#     value = models.PositiveIntegerField(verbose_name="Цена в копейках")

#     class Meta:
#         verbose_name = "Цена"
#         verbose_name_plural = "Цены"

#     def __str__(self) -> str:
#         return str(self.product)


class ReceiptsStatusModel(models.Model):
    """ Статусы фискализации чеков """

    id = models.CharField(verbose_name="id", max_length=100, null=True, blank=True)
    externalId = models.UUIDField(verbose_name="Внешний ID", default=uuid.uuid4, primary_key=True)
    createdAt = models.DateTimeField(verbose_name="Дата создания", null=True, blank=True)
    STATUS_VALUES = (
        ("PENDING", "В очереди"),
        ("IN_PROGRESS", "Выполняется"),
        ("SUCCESS", "Завершено успешно"),
        ("ERROR", "Завершено с ошибкой"),
    )
    status = models.CharField(verbose_name="Статус", choices=STATUS_VALUES, null=True, blank=True, max_length=50)

    cash_receipt = models.JSONField(verbose_name="Чек", null=True, blank=True)

    class Meta:
        ordering = ('-createdAt',)
        verbose_name = "Фискализация чека"
        verbose_name_plural = "Фискализация чеков"

    def __str__(self) -> str:
        return str(self.externalId)

