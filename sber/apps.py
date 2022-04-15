from tabnanny import verbose
from django.apps import AppConfig


class SberConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sber'
    verbose_name = 'Эквайринг Сбер'


