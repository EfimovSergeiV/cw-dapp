from enum import unique
from itertools import product
import uuid
from django.db import models
from django.utils import timezone


class CustomerModel(models.Model):
    """ Модель заказа """

    uuid = models.UUIDField(verbose_name="Идентифиактор", default=uuid.uuid4, unique=True, editable=False)
    date_created = models.DateTimeField(verbose_name="Дата создания заказа", default=timezone.now)
    order_number = models.CharField(verbose_name="Номер заказа", null=True, blank=True, max_length=15)
    
    adress = models.CharField(verbose_name="Адрес магазина", max_length=150)
    position_total = models.PositiveIntegerField(verbose_name="Сумма по позициям", default=0)
    total = models.PositiveIntegerField(verbose_name="Итог заказа", default=0)
    promocode = models.CharField(verbose_name="Промокод", max_length=120, null=True, blank=True)

    online_pay = models.BooleanField(verbose_name="Оплачен онлайн", default=False)
    payment_uuid = models.UUIDField(verbose_name="Идентификатор оплаты", null=True, blank=True)
    per_online_pay = models.BooleanField(verbose_name="Разрешение на оплату онлайн", default=False)
    seller_comm = models.TextField(verbose_name="Комментарий продавца", blank=True, null=True)

    # Информация о доставке
    delivery = models.BooleanField(verbose_name="Доставка", default=False,)
    delivery_adress = models.CharField(verbose_name="Адрес доставки", default="Самовывоз", null=True, blank=True, max_length=150)
    delivery_summ  = models.PositiveIntegerField(verbose_name="Расчитанная сумма доставки", null=True, blank=True)

    # Файлы клиентов ИП
    file = models.FileField(verbose_name="Файл с реквизитами", upload_to="orders/", null=True, blank=True)

    # легаси для ИП: Позже удалить, т.к. теперь файлик с данными прикрепляется к заказу
    person = models.CharField(verbose_name="Клиент", max_length=150, null=True, blank=True)
    phone = models.CharField(verbose_name="Телефон клиента", null=True, blank=True, max_length=40)
    email = models.EmailField(verbose_name="Электронная почта", null=True, blank=True)
    comment = models.TextField(verbose_name="Комментарий к заказу", null=True, blank=True, max_length=2500)

    company = models.CharField(verbose_name="Название компании", max_length=150, null=True)
    legaladress = models.CharField(verbose_name="Юридический адрес", max_length=150, null=True)
    inn = models.CharField(verbose_name="ИНН", max_length=150, null=True)
    kpp = models.CharField(verbose_name="КПП", max_length=150, null=True)
    okpo = models.CharField(verbose_name="ОКПО", max_length=150, null=True)
    bankname = models.CharField(verbose_name="Наименование банка", max_length=150, null=True)
    currentacc = models.CharField(verbose_name="Расчетный счет", max_length=150, null=True)
    corresponding = models.CharField(verbose_name="Корреспондентский счет", max_length=150, null=True)
    bic = models.CharField(verbose_name="БИК", max_length=150, null=True)

    # Статусы заказов
    ORDER_STATUS = (
        ("notprocessed", "не обработан"),
        ("inprocessed", "в обработке"),
        ("processed", "обработан"),
        ("awaitingpayment", "ожидает оплаты"),
        ("delivery", "доставка ТК"),
        ("waitingclient", "ожидает клиента"),
        ("completed", "выполнен"),
        ("notcompleted", "не выполнен"),
    )

    status = models.CharField(verbose_name="Статус заказа", max_length=100, choices=ORDER_STATUS, default="notprocessed")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return self.order_number


class OrderedProductModel(models.Model):
    """ 
        Модель заказанного товара 
        Может потребоваться проверка на актуальную стоимость товара в момент заказа, 
        ибо в JS можно поменять переменную стоимости    
    """

    customer = models.ForeignKey(CustomerModel, related_name="client_product", verbose_name="Заказчик", on_delete=models.CASCADE)
    product_id = models.PositiveIntegerField(verbose_name="Идентификатор товара", default=0)
    vcode = models.CharField(verbose_name="Артикул", max_length=100)
    name = models.CharField(verbose_name="Наименование", max_length=300)
    # rating
    price = models.CharField(verbose_name="Стоимость (RUB)", max_length=150)
    preview_image = models.URLField(verbose_name="Изображение", null=True, blank=True, default="https://glsvar.ru/img/c/preview/notpreviewimg.png")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    
    class Meta:
        verbose_name = "Заказанный товар"
        verbose_name_plural = "Заказанные товары"

    def __str__(self):
        return self.name


class RequestPriceModel(models.Model):
    """ Запрос стоимости товара """

    completed = models.BooleanField(verbose_name="Запрос выполнен", default=False)
    uuid = models.UUIDField(verbose_name="Уникальный идентификатор", default=uuid.uuid4, editable=False)
    city = models.CharField(verbose_name="Город", max_length=150)
    contact = models.CharField(verbose_name="Контакт клиента", max_length=40)
    product = models.CharField(verbose_name="Наименование товара", max_length=400)

    class Meta:
        verbose_name = "Запрос стоимости"
        verbose_name_plural = "Запросы стоимости"

    def __str__(self):
        return self.product


# Нижние модели готовить на удаление

class ClientModel(models.Model):
    """ Заказ """
    # Юридическое лицо
    legaladress = models.CharField(verbose_name="Юридический адрес", max_length=100, null=True, blank=True)
    inn = models.CharField(verbose_name="ИНН", max_length=100, null=True, blank=True)
    kpp = models.CharField(verbose_name="КПП", max_length=100, null=True, blank=True)
    okpo = models.CharField(verbose_name="ОКПО", max_length=100, null=True, blank=True)
    bankname = models.CharField(verbose_name="Наименование банка", max_length=100, null=True, blank=True)
    currentacc = models.CharField(verbose_name="Расчетный счет", max_length=100, null=True, blank=True)
    corresponding = models.CharField(verbose_name="Корреспондентский счет", max_length=100, null=True, blank=True)
    bic = models.CharField(verbose_name="БИК", max_length=100, null=True, blank=True)
    company = models.CharField(verbose_name="Название компании", max_length=100, null=True, blank=True)

    # Общие
    order_numer = models.CharField(verbose_name="Номер заказа", max_length=8)
    person = models.CharField(verbose_name="Персона", max_length=100, null=True, blank=True)
    phone = models.CharField(verbose_name="Телефон", max_length=20)
    email = models.EmailField(verbose_name="Email", null=True, blank=True)

    region_code = models.CharField(verbose_name="Код региона", max_length=10)
    adress = models.TextField(verbose_name="Адрес", max_length=300)
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True, max_length=1000)
    total = models.PositiveIntegerField(verbose_name="Общая сумма", null=True, blank=True, default=None)

    # Статусы заказов
    ORDER_STATUS = (
        ("не обработан", "не обработан"),
        ("обработан", "обработан"),
        ("выполнен", "выполнен"),
        ("не выполнен", "не выполнен"),
    )
    
    status = models.CharField(verbose_name="Статус", max_length=100, choices=ORDER_STATUS, default="не обработан")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return self.order_numer


class OrderedGoodsModel(models.Model):
    """ Заказанный товар"""
    #Информация о заказанном товаре
    client = models.ForeignKey(ClientModel, 
        related_name="client_product", 
        verbose_name="Заказчик", 
        on_delete=models.CASCADE)
    vcode = models.CharField(verbose_name="Артикул", max_length=100)
    previewImage = models.URLField(verbose_name="Изображение", default="https://glsvar.ru/img/c/preview/notpreviewimg.png")    
    name = models.CharField(max_length=100, verbose_name="Название")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.PositiveIntegerField(verbose_name="Стоимость", 
        help_text= "Стоимость на момент заказа(технически может отличаться от текущей)")

    class Meta:
        verbose_name = "Заказанный товар"
        verbose_name_plural = "Заказанные товары"

    def __str__(self):
        return self.name
    

class PromocodeModel(models.Model):
    """ Промокоды для скидок """

    MODS = (
        ("ct", "Категории товаров"),
        ("prod", "Идентификаторы товаров"),
    )

    promocode = models.CharField(verbose_name="Промокод", max_length=30, null=True, blank=True)
    value = models.PositiveIntegerField(verbose_name="Размер скидки, %", default=0)
    mod = models.CharField(verbose_name='Модификатор', max_length=10, choices=MODS, default="ct")
    products = models.CharField(verbose_name="Список товаров", max_length=5000, help_text="Идентификаторы товаров или категорий товаров через запятую", null=True, blank=True)
    start_date = models.DateTimeField(verbose_name="Начало действия")
    end_date = models.DateTimeField(verbose_name="Окончание действия")

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self) -> str:
        return str(self.promocode)



class ReviewModel(models.Model):
    """ Отзывы пользователей """

    activated = models.BooleanField(verbose_name="Активирован", default=True)
    product_id = models.PositiveIntegerField(verbose_name="ID товара", default=0)
    user_name = models.CharField(verbose_name="Имя", default="Пользователь", null=True, blank=True, max_length=100)
    r_text = models.TextField(verbose_name="Отзыв", null=True, blank=True, max_length=1000)
    rating = models.PositiveIntegerField(verbose_name="Оценка", default=5)
    date = models.DateField(verbose_name="Дата", default=timezone.now )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-date",]

    def __str__(self):
        return self.user_name