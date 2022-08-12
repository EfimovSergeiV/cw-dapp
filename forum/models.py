from django.db import models
from django.utils import timezone


class CategoryModel(models.Model):
    """ Категории форума """

    activated = models.BooleanField(verbose_name="Активирован", default=False)
    name = models.CharField(verbose_name="Название категории", max_length=60)
    description = models.TextField(verbose_name="Описание категории", max_length=2000)
    position = models.PositiveIntegerField(verbose_name="Позиция", default=0)
   
    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"
        ordering = ['position',]


    def __str__(self) -> str:
        return self.name


class TopicModel(models.Model):
    """ Модель тем категорий """

    category = models.ForeignKey(CategoryModel, verbose_name="Категория", related_name="topic", on_delete=models.CASCADE)
    activated = models.BooleanField(verbose_name="Активирован", default=True)
    created_date = models.DateField(verbose_name="Дата создания", default=timezone.now)
    username = models.CharField(verbose_name="Пользователь", max_length=60, default="Гость")
    title = models.CharField(verbose_name="Название темы", max_length=120)
    description = models.TextField(verbose_name="Описание темы", max_length=5000)
    
    
    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"
        ordering = ['id',]

    def __str__(self) -> str:
        return self.title


class PostModel(models.Model):
    """ Модель постов фоорума """

    topic = models.ForeignKey(TopicModel, verbose_name="Тема", related_name="post", on_delete=models.CASCADE)
    activated = models.BooleanField(verbose_name="Активирован", default=True)
    created_date = models.DateField(verbose_name="Дата создания", default=timezone.now)
    username = models.CharField(verbose_name="Пользователь", max_length=60, default="Гость")
    post = models.TextField(verbose_name="Сообщение", max_length=5000)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ['id',]


    def __str__(self) -> str:
        return str(self.username)