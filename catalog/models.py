from os import name
from django.db import models
from django.db.models.base import Model, ModelState
from easy_thumbnails.fields import ThumbnailerImageField
from main.models import AbsDateModel, AbsActivatedModel, AbsProductModel
from mptt.models import MPTTModel, TreeForeignKey
from content.models import *
from main.models import *


class CityModel(models.Model):
    """ 
    Модель городов в которых есть магазины
    Используется для шапки (Header) и определения города пользователя
    """
    city = models.CharField(verbose_name="Город", max_length=100)
    zip = models.CharField(verbose_name="Индекс", max_length=8)
    phone = models.CharField(verbose_name="Телефон", max_length=60)
    phone_link = models.CharField(verbose_name="Ссылка телефона", max_length=60)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return self.city


class ShopAdressModel(models.Model):
    UID = models.CharField(verbose_name="Идентификатор 1С", null=True, blank=True, max_length=100)
    email = models.EmailField(verbose_name="Электронный адрес")
    telegram = models.CharField(verbose_name="Телеграмм", max_length=100, null=True, blank=True)
    whatsapp = models.CharField(verbose_name="WhatsApp", max_length=100, null=True, blank=True)
    viber = models.CharField(verbose_name="Viber", max_length=100, null=True, blank=True)

    position = models.PositiveIntegerField(verbose_name="Позиция в списке", default=0)
    region_code = models.CharField(verbose_name="Код региона", default='PSK', max_length=3)

    delivery_inside = models.CharField(verbose_name="Доставка по городу", max_length=250, null=True, blank=True)
    delivery_outside = models.CharField(verbose_name="Доставка за городом", max_length=250, null=True, blank=True)

    city = models.CharField(verbose_name="Город", max_length=100)
    zip = models.CharField(verbose_name="Индекс", null=True, blank=True, max_length=8)
    adress = models.TextField(verbose_name="Адрес", max_length=500)
    phone = models.CharField(verbose_name="Телефон", max_length=60)
    maps = models.URLField(verbose_name="Ссылка на YandexMaps")
    google_maps = models.CharField(verbose_name="Ссылка на Google Maps", max_length=500, null=True)
    wday = models.CharField(verbose_name="График по будням", null=True, blank=True, max_length=60)
    wend = models.CharField(verbose_name="График по выходным", null=True, blank=True, max_length=60)


    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"
        ordering = ['position',]

    def __str__(self):
        return self.adress


class CategoryModel(MPTTModel, AbsActivatedModel):
    """Подкатегории каталога"""
    name = models.CharField(verbose_name="Название", max_length=100)
    description = models.TextField(verbose_name="Описание", max_length=1000, default="Нет описания", null=True, blank=True)
    parent = TreeForeignKey('self', verbose_name="Вложенность", on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        
    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return str(self.id) + '. ' + self.name


class BrandProductModel(models.Model):
    brand = models.CharField(verbose_name="Бренд", max_length=160)
    carousel = models.BooleanField(verbose_name="Отображать", default=False)
    image = models.ImageField(verbose_name="Изображение", help_text="Разрешение изображения 1024x480", upload_to="img/c/brand/")
    description = models.TextField(verbose_name="Описание", max_length=1000, null=True, blank=True)
    priority = models.IntegerField(verbose_name="Приоритет выдачи в каталоге", default=50)

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.brand


class ProductModel(AbsProductModel):
    """ Товары """   
    category = models.ForeignKey(CategoryModel, related_name='product_category', verbose_name="Категория" , null=True, blank=True, on_delete=models.SET_NULL)
    brand = models.ForeignKey(BrandProductModel, related_name="brand_product", verbose_name="Бренд", null=True, blank=True, on_delete=models.SET_NULL)

    preview_image = ThumbnailerImageField(
        verbose_name="",
        resize_source=dict(size=(235, 177)),
        help_text="Миниатира товара ( 235x177 px)", 
        blank=True, 
        null=True, upload_to="img/c/preview/")
    recommend = models.BooleanField(verbose_name="Рекомендуемый", default=False)
    rating = models.DecimalField(verbose_name="Рейтинг", default=3, max_digits=3, decimal_places=1)

    UID = models.CharField(
        verbose_name="Идентификатор 1С", 
        null=True, 
        blank=True, 
        unique=True, 
        max_length=100)

    keywords = models.TextField(
        verbose_name="Ключевые слова", max_length=500, null=True, blank=True,
        help_text="Ключевые слова для поиска, лучше через запятую."
    )
    related = models.ManyToManyField(CategoryModel, blank=True, verbose_name="Категории", related_name="related_ct")

    promo = models.BooleanField(default=False, verbose_name="Скидка")
    promo_code = models.CharField(verbose_name="Промокод", null=True, blank=True, max_length=100)
    discount = models.PositiveIntegerField(
        verbose_name="Старая цена", 
        null=True, 
        blank=True, 
        help_text="Сюда заносим старую цену, новую пишем в цены")

    """ Мигрируем с распределённых стоимостей товара, в единственную """
    CCY_VAL = (
        ("RUB", "RUB"),
        ("EUR", "EUR"),
        ("USD", "USD"),
        ("CNY", "CNY"),
    )

    EXISTENCE = (
        ("stock", "в наличии"),
        ("order", "под заказ"),
    )

    only_price_status = models.BooleanField(verbose_name="Общая стоимость", default=False)
    only_price = models.FloatField(verbose_name="Стоимость", default=0, null=True, blank=True)
    currency = models.CharField(verbose_name="Валюта", max_length=10, choices=CCY_VAL, default="RUB")
    status = models.CharField(verbose_name="Наличие на складе", max_length=100, choices=EXISTENCE, default="order")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        unique_together = ['name',]
        ordering = ['name',]

    def __str__(self):
        return str(self.id) + ') ' + self.name


class ProductKeywordModel(models.Model):
    """ Ключевые слова для поиска товаров """
    product = models.ForeignKey(ProductModel, related_name="prod_keywords", verbose_name="Товар", on_delete=models.CASCADE)
    keyword = models.CharField(verbose_name="Ключевое слово", max_length=200)

    class Meta:
        verbose_name = "Ключевое слово"
        verbose_name_plural = "Ключевые слова"

    def __str__(self):
        return self.keyword


class ProductSetModel(AbsProductModel):
    """ Связанные комплектации продуктов (!)"""
    product = models.ForeignKey(ProductModel, related_name="product_set", verbose_name="Основной продукт", on_delete=models.CASCADE)
    price = models.FloatField(verbose_name="Стоимость товара", default=0)
    link = models.URLField(verbose_name="Ссылка на товар", null=True, blank=True)
    UID = models.CharField(verbose_name="Идентификатор 1С", null=True, blank=True, max_length=100)
    preview_image = ThumbnailerImageField(
        verbose_name="",
        resize_source=dict(size=(235, 177)),
        help_text="Миниатира товара ( 235x177 px)", 
        blank=True, 
        null=True, upload_to="img/c/preview/")

    class Meta:
        verbose_name = "Комплект товара"
        verbose_name_plural = "Комплекты товаров"

    def __str__(self):
        return self.name


class ProductCompModel(models.Model):
    """
    Составные части много составного товара, ссылаются на существующие товары,
    и могут обслуживаться из 1С с помощью API 
    """
    product = models.ForeignKey(ProductModel, related_name="product_comp", verbose_name="Основной продукт", on_delete=models.CASCADE)
    rel_id = models.PositiveIntegerField(
        verbose_name="ID связанного товара",
        help_text=
        """
        Уникальный идентификатор составного товара,
        можно узнать в таблице списка товаров или по последним цифрам URL
        в карточке товара, непосредственно на сайте (FrontEnd)
        """)
    completed = models.BooleanField(
        verbose_name="Находится в текущей комплектации",
        default=True,
        )

    class Meta:
        verbose_name = "Составная часть товара"
        verbose_name_plural = "Составные части товаров"

    def __str__(self):
        return str('https://glsvar.ru/product/') + str(self.rel_id)


class ExternalLinkModel(models.Model):
    """Внешние ссылки товаров"""
    product = models.ForeignKey(ProductModel, verbose_name="Товар", related_name="prod_link", on_delete=models.CASCADE)   
    name = models.CharField(verbose_name="Заголовок ссылки", max_length=150)
    description = models.TextField(verbose_name="Описание", default="Нет описания", null=True, blank=True, max_length=500)
    url = models.URLField(verbose_name="Внешняя ссылка", help_text="Будет оттображаться в документах карточки товара")

    class Meta:
        verbose_name = "Внешняя ссылка"
        verbose_name_plural = "Внешние ссылки"

    def __str__(self):
        return self.name


class DocumentModel(models.Model):
    """ Документы к товарам """
    product = models.ForeignKey(ProductModel, verbose_name="Товар", related_name="prod_doc", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название", max_length=100)
    description = models.TextField(verbose_name="Описание", default="Нет описания", null=True, blank=True, max_length=500)
    doc = models.FileField(verbose_name="Документ", upload_to="img/c/doc/")

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return self.name


class PropsNameModel(AbsActivatedModel):
    """ 
    Свойства товаров для подсказки фильтрам по товарам
    Привязана к категориям товаров
    """
    PROPWIDGET = (
        ('value', 'Значение'),
        ('range', 'Диапазон'),
    )
    position = models.PositiveIntegerField(verbose_name="Позиция в списке", default=0)
    name = models.CharField(verbose_name="Название", max_length=100)
    propwidget = models.CharField(verbose_name="Виджет фильтра", choices=PROPWIDGET, default='value' ,max_length=60)
    prop_alias = models.CharField(
        verbose_name="Алиас",
        help_text="""
        Должен быть уникальным, и содержать 4 символа (A-Za-z1-9)
        Можно использовать значение из генератора справа.
        """,
        unique=True,
        max_length=4)
    category = models.ManyToManyField(CategoryModel, verbose_name="Категории", related_name="prop_ct")
    description = models.TextField(verbose_name="Описание", null=True, blank=True, max_length=4000)

    class Meta:
        verbose_name = "Свойство категории"
        verbose_name_plural = "Свойства категорий"

    def __str__(self):
        return self.name


class PropOpsModel(models.Model):
    """ 
    Варианты значений свойств для подсказки фильтрам
    Связана с PropsNameModel
    """
    name = models.ForeignKey(PropsNameModel, 
        verbose_name="Название свойства", 
        related_name='prop_ops',
        on_delete=models.CASCADE)
    ops = models.CharField(
        verbose_name="Отображаемое значение свойства",
        help_text="Текст который будет видеть пользователь",
        null=True, blank=True ,max_length=60)
    opskey = models.CharField(
        verbose_name="Псевдоним свойства",
        help_text="Ключ базы данных по которому фактически будет происходить поиск",
        null=True, blank=True, max_length=8
    )

    class Meta:
        verbose_name = "Возможное значение"
        verbose_name_plural = "Возможные значения для пользовательского фильтра"

    def __str__(self):
        return str(self.name)


class PropStrModel(models.Model):
    """
    Свойство товара в виде строки
    Привязанное к товару
    """

    name = models.CharField(verbose_name="Название свойства",  max_length=100)
    product = models.ForeignKey(
        ProductModel,
        verbose_name="Продукт",
        related_name="%(class)s",
        null=True,
        on_delete=models.SET_NULL)

    value = models.CharField(verbose_name="Значение свойства", max_length=200)
    qname = models.CharField(
        verbose_name="Псевдоним названия",
        # choices=options(), ДОБАВИТЬ ЗНАЧЕНИЕ ПО УМОЛЧАНИЮ ИЗ МОДЕЛИ
        help_text=
        """
        Псевдоним названия свойства,используется только для фильтрации. 
        Допускаются: (a-zA-Z1-9), желательно 4 символа
        Пример:
        abCD, b4F3 ...или DF4e
        """, 
        max_length=4, null=True, blank=True)

    qvalue = models.CharField(
        verbose_name="Псевдоним значения",
        # choices=options(), ДОБАВИТЬ ЗНАЧЕНИЕ ПО УМОЛЧАНИЮ ИЗ МОДЕЛИ
        help_text=
        """
        Псевдоним значения свойства,используется только для фильтрации. 
        Допускаются: (a-zA-Z1-9). желательно 8 символов
        Пример:
        55-70, mma ...или TIG84
        """, 
        max_length=8, null=True, blank=True)

    class Meta:
        verbose_name = "Свойство товара"
        verbose_name_plural = "Свойства товаров"
        ordering = ['qname',]

    def __str__(self):
        return self.name


class AvailableModel(models.Model):
    """
    Подготовить модель к объеденению
    """
    EXISTENCE = (
        ("stock", "в наличии"),
        ("order", "под заказ"),
    )
    shop = models.ForeignKey(ShopAdressModel, related_name='shop_available', verbose_name="Магазин", null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(ProductModel, related_name='prod_available', verbose_name="Продукт", on_delete=models.CASCADE)
    status = models.CharField(verbose_name="Наличие на складе", max_length=100, choices=EXISTENCE, default="order")
    quantity = models.FloatField(verbose_name="Количество", default=0,  help_text="Остаток на складе")

    class Meta:
        verbose_name = "Наличие товара в магазине"
        verbose_name_plural = "Наличие товаров в магазинах"

    def __str__(self):
        return self.status


class PriceModel(models.Model):
    """
     Стоимость и наличие товара в магазинах
     Объединить стоимость и наличие товара в одну модель, не теряя обратной совместимости.
    """

    EXISTENCE = (
        ("stock", "в наличии"),
        ("order", "под заказ"),
    )

    CCY_VAL = (
        ("RUB", "RUB"),
        ("EUR", "EUR"),
        ("USD", "USD"),
    )

    shop = models.ForeignKey(ShopAdressModel, related_name='shop_price',verbose_name="Магазин", null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(ProductModel, related_name='prod_price', verbose_name="Продукт", on_delete=models.CASCADE)

    verified = models.BooleanField("Проверен", default=False)
    price = models.FloatField(verbose_name="Стоимость товара", default=0)
    quantity = models.FloatField(verbose_name="Остаток на складе", default=0,  help_text="Остаток на складе")
    status = models.CharField(verbose_name="Наличие на складе", max_length=100, choices=EXISTENCE, default="order")

    currency = models.CharField(verbose_name="Валюта", max_length=10, choices=CCY_VAL, default="RUB")

    def vcode_product(self):
        """Возвращаем артикул в админку"""
        return self.product.vcode

    class Meta:
        verbose_name = "Стоимость товара"
        verbose_name_plural = "Цены на товар"

    def __str__(self):
        return str(self.price)


class ProductFeedbackModel(AbsDateModel, AbsActivatedModel):
    """Отзывы о продукте"""
    product = models.OneToOneField(ProductModel, related_name='prod_feedback', verbose_name="Продукт", on_delete=models.CASCADE)
    email = models.EmailField(verbose_name="Электронная почта")
    user = models.CharField(verbose_name="Никнейм", max_length=150)
    feedback = models.TextField(verbose_name="Отзыв")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return self.product


class ProductImageModel(AbsDateModel):
    """Все изображения каталога"""
    name = models.CharField(verbose_name="Название", default="Изображение", null=True, blank=True, max_length=100)
    image = ThumbnailerImageField(
        verbose_name = '',
        help_text="Список изображений товаров 640x480",
        resize_source=dict(size=(640, 480)),
        upload_to="img/c/prod/")
    product = models.ForeignKey(ProductModel, related_name="prod_img", verbose_name="Продукт", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return self.name


class CatalogFileModel(models.Model):
    name = models.CharField(verbose_name="Название файла", max_length=50)
    description = models.TextField(
        verbose_name="Описание/Комментарий", 
        help_text="Не будет отображаться на сайте, нужна для внутреннего пользования", 
        default="Нет описания", 
        max_length=500)
    file = models.FileField(verbose_name="Файл", upload_to='c/')

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    def __str__(self):
        return self.name