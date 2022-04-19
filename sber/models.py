from tabnanny import verbose
from django.db import models



# class AccountModel(models.Model):
#     """ Данные аккаунта интеграции """

#     activated = models.BooleanField(verbose_name="Активирован", default=False)
#     gateway = models.URLField(verbose_name="Платёжный шлюз")
#     user_name = models.CharField(verbose_name="Логин", max_length=50)
#     password = models.CharField(verbose_name="Пароль", max_length=50)

#     class Meta:
#         verbose_name = "Аккаунт"
#         verbose_name_plural = "Аккаунты"

#     def __str__(self) -> str:
#         return self.user_name