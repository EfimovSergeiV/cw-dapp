from django.db import models
# from django.db.models.base import Model, ModelState
from django.utils import timezone
from django_resized import ResizedImageField

from easy_thumbnails.fields import ThumbnailerImageField  # Migrate to ResizedImageField
"""
Django==5.1

    from catalog.models import ProductModel
  File "/home/anon/glsvar-ru/cw-dapp/catalog/models.py", line 4, in <module>
    from easy_thumbnails.fields import ThumbnailerImageField  # Migrate to ResizedImageField
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/anon/glsvar-ru/cw-dapp/venv/lib/python3.11/site-packages/easy_thumbnails/fields.py", line 2, in <module>
    from easy_thumbnails import files
  File "/home/anon/glsvar-ru/cw-dapp/venv/lib/python3.11/site-packages/easy_thumbnails/files.py", line 13, in <module>
    from easy_thumbnails import engine, exceptions, models, utils, signals, storage
  File "/home/anon/glsvar-ru/cw-dapp/venv/lib/python3.11/site-packages/easy_thumbnails/storage.py", line 1, in <module>
    from django.core.files.storage import FileSystemStorage, get_storage_class
ImportError: cannot import name 'get_storage_class' from 'django.core.files.storage' (/home/anon/glsvar-ru/cw-dapp/venv/lib/python3.11/site-packages/django/core/files/storage/__init__.py)
^C% 
"""



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
    mobile = models.CharField(verbose_name="Моб. телефон", max_length=60, null=True, blank=True)
    maps = models.URLField(verbose_name="Ссылка на YandexMaps")
    google_maps = models.CharField(verbose_name="Ссылка на Google Maps", max_length=500, null=True)
    wday = models.CharField(verbose_name="График по будням", null=True, blank=True, max_length=60)
    wend = models.CharField(verbose_name="График по выходным", null=True, blank=True, max_length=60)


    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "1. Магазины"
        ordering = ['position',]

    def __str__(self):
        return self.adress


class CategoryModel(MPTTModel, AbsActivatedModel):
    """Подкатегории каталога"""
    image = ResizedImageField(
        size = [120, 85],
        verbose_name="",
        crop = ['middle', 'center'],
        upload_to='img/c/preview/',
        help_text="Миниатира категории, только первого уровня (120x85 px)",
        quality=100,
        null=True,
        blank=True,
        force_format='WEBP',
    )
    name = models.CharField(verbose_name="Название", max_length=100)
    description = models.TextField(verbose_name="Описание", max_length=1000, default="Нет описания", null=True, blank=True)
    parent = TreeForeignKey('self', verbose_name="Вложенность", on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    visible = models.BooleanField(verbose_name="Отображать в категориях", default=True)
    related = models.ManyToManyField('self', verbose_name='Связанные категории', blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "3. Категории"
        
    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return str(self.id) + '. ' + self.name


class BrandProductModel(models.Model):
    brand = models.CharField(verbose_name="Бренд", max_length=160)
    carousel = models.BooleanField(verbose_name="Отображать в карусели", default=False)
    image = ResizedImageField(
        size = [206, 80],
        verbose_name="",
        crop = ['middle', 'center'],
        upload_to='img/c/brand/',
        help_text="Размеры логотипа (206x80 px)",
        quality=100,
        null=True,
        blank=True,
        force_format='WEBP',
    )
    description = models.TextField(verbose_name="Описание", max_length=1000, null=True, blank=True)
    priority = models.IntegerField(verbose_name="Приоритет выдачи в каталоге", default=50)

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "2. Бренды"
        ordering = ['-priority',]

    def __str__(self):
        return self.brand


class ProductModel(AbsProductModel):
    """ Товары """   
    category = models.ForeignKey(CategoryModel, related_name='product_category', verbose_name="Категория" , null=True, blank=True, on_delete=models.SET_NULL)
    brand = models.ForeignKey(BrandProductModel, related_name="brand_product", verbose_name="Бренд", null=True, blank=True, on_delete=models.SET_NULL)

    preview_image = ResizedImageField(
        size = [235, 177],
        verbose_name="",
        crop = ['middle', 'center'],
        upload_to='img/c/preview/',
        help_text="Миниатира товара (235x177 px)",
        quality=100,
        default='img/c/preview/noimage.webp',
        force_format='WEBP',
    )

    recommend = models.BooleanField(verbose_name="Рекомендуемый", default=False)
    show_more = models.BooleanField(verbose_name="Показывать чаще", default=False)
    rating = models.DecimalField(verbose_name="Рейтинг", default=3, max_digits=3, decimal_places=1)

    UID = models.CharField(
        verbose_name="Идентификатор 1С", 
        null=True, 
        blank=True, 
        unique=True, 
        max_length=100)

    keywords = models.CharField(
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
    only_price = models.IntegerField(verbose_name="Стоимость", default=0, null=True, blank=True)
    currency = models.CharField(verbose_name="Валюта", max_length=10, choices=CCY_VAL, default="RUB")
    status = models.CharField(verbose_name="Наличие на складе", max_length=100, choices=EXISTENCE, default="order")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "5. Товары"
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
        verbose_name_plural = "4. Свойства категорий"

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
        verbose_name_plural = "8. Файлы"

    def __str__(self):
        return self.name
    

# from django.contrib.gis.db import models as gis_models
class ExtendedProductModel(models.Model):
    """ Товары для расширенного поиска (каталога) """

    name = models.CharField(verbose_name="Название", max_length=200)
    city = models.CharField(verbose_name="Город", max_length=100)
    shop_id = models.IntegerField(verbose_name="ID магазина", null=True, blank=True)
    shop = models.CharField(verbose_name="Магазин", max_length=100)
    card_link = models.JSONField(verbose_name="Ссылка на карточку товара", null=True, blank=True)
    price = models.IntegerField(verbose_name="Цена", null=True, blank=True)
    quantity = models.IntegerField(verbose_name="Количество", null=True, blank=True)
    last_update = models.DateTimeField(verbose_name="Последнее обновление", auto_now=True)

    class Meta:
        verbose_name = "Товар расширенного каталога"
        verbose_name_plural = "6. Товары расширенного каталога"

    def __str__(self):
        return self.name
    


import pandas as pd
from django.db.models import Q

class ImportExtendedProductsModel(models.Model):
    """ Импорт товаров xls из экспорта 1С """

    """ SHOPS
        Псков, ул.Леона Поземского, 92, Павильон 28 (рынок на Алмазной)
        Псков, ул.Шоссейная д.3а
        Псков, пос. Неёлово,
        Великие Луки, проспект Ленина д.57    
        Смоленск, ул. Посёлок Тихвинка 69, ТК "Город Мастеров" павильон №73
        Петрозаводск, ул. Заводская, д. 2

    """

    SHOPS = (
        ('1', 'ул.Леона Поземского, 92, Павильон 28 (рынок на Алмазной)'),
        ('2', 'ул.Шоссейная д.3а'),
        ('3', 'пос. Неёлово, ул.Юбилейная д. 5ж'),
        ('4', 'проспект Ленина д.57'),
        ('5', 'ул. Посёлок Тихвинка 69, ТК "Город Мастеров" павильон №73'),
        ('6', 'ул. Заводская, д. 2'),
    )


    created_date = models.DateField(verbose_name="Дата выгрузки", auto_now=True)
    shop = models.CharField(verbose_name="Магазин", choices=SHOPS, max_length=100, null=True, blank=True)
    file = models.FileField(verbose_name="Файл xls", upload_to='c/import-1c/')

    class Meta:
        verbose_name = "Таблица импорта с товаром"
        verbose_name_plural = "7. Таблицы импорта с товарами"

    def __str__(self):
        # return shop value from tuple and created date
        return self.get_shop_display() + ' - ' + str(self.created_date)

    def save(self, *args, **kwargs):
        super(ImportExtendedProductsModel, self).save(*args, **kwargs)
        SHOPS = {
            "1": "Псков",
            "2": "Псков",
            "3": "Псков",
            "4": "Великие Луки",
            "5": "Смоленск",
            "6": "Петрозаводск",
        }

        prods_qs = ExtendedProductModel.objects.filter(shop=self.get_shop_display())
        prods_updated = []
        
        # печатаем полный путь к файлу self.file.path
        df = pd.read_excel(f'{self.file.path}', sheet_name='TDSheet', header=None, index_col=0)
        for index, row in df.iterrows():

            # Обновляем или создаём товар
            price = row[12] if type(row[12]) == int else None
            quantity = row[13] if type(row[13]) == int else None

            if price and quantity:

                tokens = str(index).replace("  ", "").split()
                conditions = Q()
                for token in tokens:
                    conditions &= Q(name__icontains=token)

                prod = prods_qs.filter(conditions)

                if prod.exists() and len(prod) == 1:
                    prod.update(
                        price=price,
                        quantity=quantity,
                        last_update=timezone.now()
                    )
                    prods_updated.append(prod[0].id)

                elif prod.exists() and len(prod) > 1:
                    # Удаляем дубликаты /// !!! ПЕРЕСМОТРЕТЬ ЛОГИКУ
                    prod.delete()

                else:
                    stat = prods_qs.create(
                        name=str(index).replace("  ", ""),
                        city=SHOPS[self.shop],
                        shop_id= self.shop,
                        shop=self.get_shop_display(),
                        price=price,
                        quantity=quantity,
                    )

                    prods_updated.append(stat.id)

                
        # Удаляем товары которых нет в обновлённых или созданных
        objects_to_delete = prods_qs.exclude(id__in=prods_updated)
        objects_to_delete.delete()

