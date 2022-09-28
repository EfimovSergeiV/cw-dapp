from unicodedata import name
from django import views
from django.contrib import admin
from django.urls import path, re_path

from orders.views import *
from orders.cdek import *

urlpatterns = [
    path('user-order/', OrderListViews.as_view()),
    path('order/', OrderViews.as_view()),
    path('request-price/', RequestPriceViews.as_view()),
    path('order-status/', OrderStatusViews.as_view()),
    path('orderinfo/<slug:order>/', OrderInfoView.as_view()),
    # path('sendmail/', MailsView.as_view()),

    # Предоставление данных в 1С
    path('list-orders/', OneSotfOrderView.as_view()),

    # CDEK API
    path('cdek/regions/', CdekRegionView.as_view()),
    path('cdek/cities/<int:region_code>/', CdekCityView.as_view()),
    path('cdek/tarifflist/', TariffListView.as_view()),
    path('order_status/<slug:uuid>/<slug:status>/', edit_order_status, name='edit_order_status'),
    path('pricerequest_close/<slug:uuid>/', price_request_status, name='edit_price_request_status'),
    path('sent_payment_email/<slug:uuid>/', send_payment_email, name='send_payment_email'),
    # path('mail_template/', mail_template, name='mail_template'),
    # path('glsvar-bot/', glsvar_bot, name='mail_template'),
    

    # Роутинг для эквайринга Сбер
    re_path('payment/register/', RegisterPaymentView.as_view()),      # Регистрация 
    re_path('payment/status/', CheckOrderPaymentView.as_view()),          # Уточняем статус
    # re_path('continue/', ContinueView.as_view())     # Продолжнение прерванной оплаты

]