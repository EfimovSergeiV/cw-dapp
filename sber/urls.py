from django.urls import path, re_path

from sber.views import *



urlpatterns = [
    # re_path('register/', RegisterOrderView.as_view()),      # Регистрация 
    # re_path('status/', OrderStatusView.as_view()),          # Уточняем статус
    # re_path('continue/', ContinuePaymentView.as_view())     # Продолжнение прерванной оплаты

    # re_path('register/', RegisterView.as_view()),      # Регистрация 
    # re_path('status/', StatusView.as_view()),          # Уточняем статус
    # re_path('continue/', ContinueView.as_view())     # Продолжнение прерванной оплаты
]
