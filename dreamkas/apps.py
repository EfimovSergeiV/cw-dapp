from tabnanny import verbose
from django.apps import AppConfig


class DreamkasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dreamkas'
    verbose_name = "DreamKas"
