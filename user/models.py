import email
from pyexpat import model
from statistics import mode
from tabnanny import verbose
from django.db import models
from django.forms import model_to_dict
from catalog.models import ProductModel
from django.contrib.auth.models import User
import uuid

class ProfileModel(models.Model):
    """ Дополнительная информация о пользователе """

    user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE)
    adress = models.CharField(verbose_name="Адрес", null=True, blank=True, max_length=200)
    phone = models.CharField(verbose_name="Телефон", null=True, blank=True, max_length=30)

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return self.user.username


class SubscriberModel(models.Model):
    """ Список подписчиков """

    email = models.EmailField(verbose_name="email", unique=True)

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

    def __str__(self) -> str:
        return self.email


class LikeProdModel(models.Model):
    """ Понравившиеся товары """

    product = models.ForeignKey(ProductModel, verbose_name="Продукт", related_name='like_prod', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Пользователь", related_name="like_user", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Любимый товар"
        verbose_name_plural = "Любимые товары"

    def __str__(self):
        return str(self.id)


class ProductReviewModel(models.Model):
    """ Отзывы пользователей о продукте """

    visible = models.BooleanField(verbose_name="Отображать", default=True)
    product = models.ForeignKey(ProductModel, verbose_name="Продукт", related_name="comment_prod", on_delete=models.CASCADE)
    # user = models.ForeignKey(User, verbose_name="Пользователь", related_name="comment_user", on_delete=models.CASCADE)
    user = models.CharField(verbose_name="Пользоваталь", default="Гость", max_length=80)

    grade = models.PositiveIntegerField(verbose_name="Оценка пользователя")
    review = models.TextField(verbose_name="Отзыв", max_length=2500, null=False, blank=False)
    date = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


    def __str__(self):
        return str(self.product)


class FeedBackModel(models.Model):
    """ Обратная связь с общей формы сообщений """

    completed = models.BooleanField(verbose_name="Вопрос проработан", default=False)
    uuid = models.UUIDField(verbose_name="Идентификатор", default=uuid.uuid4, editable=False)
    city = models.CharField(verbose_name="Город", max_length=100, null=True, blank=True)
    person = models.CharField(verbose_name="Клиент", max_length=150, null=True, blank=True)
    contact = models.CharField(verbose_name="Контакт", max_length=150, null=True, blank=True)
    theme = models.CharField(verbose_name="Тематика", max_length=150, null=True, blank=True)
    text = models.TextField(verbose_name="Сообщение", max_length=5000)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return str(self.person)