from django.utils.safestring import mark_safe
from django.contrib import admin
from orders.models import *


class OrderedProductInline(admin.TabularInline):
    model = OrderedProductModel
    readonly_fields = ('vcode', 'name', 'product_id', 'quantity',)
    fieldsets = (
        (None, {'fields': ('vcode', 'product_id', 'name', 'price', 'quantity',)}),
        )
    extra = 0


class CustomerAdmin(admin.ModelAdmin):
    inlines = ( OrderedProductInline, )

    def send_payment_mail(self, obj):
        return mark_safe(
            '''
            <a style="background-color: #73ff54; padding: 7px; color: #3b3b3b; border-radius: 3px;" href="/o/sent_payment_email/%s/">
            <b>📩 ОТПРАВИТЬ ПИСЬМО НА ОПЛАТУ</b></a>
            '''
            % (obj.uuid))

    send_payment_mail.short_description = 'Действия'

        
    list_display = ('online_pay', 'order_number', 'phone', 'date_created', 'status')
    list_display_links = ('online_pay', 'order_number', 'phone', 'date_created',)
    list_editable = ('status', )
    readonly_fields = (
        'order_number', 'date_created', 'adress', 'delivery_adress',
        'person', 'phone', 'email', 'comment', 'delivery', 'send_payment_mail',
        'company', 'legaladress', 'inn', 'kpp', 'okpo', 'bankname',
        'currentacc', 'corresponding', 'bic', 'online_pay', 'payment_uuid', 'uuid',
        )
    fieldsets = (
        ("Заказ", {'fields': ( 'uuid', ('status', 'date_created'), ('order_number', 'position_total', 'total',), ('send_payment_mail', 'per_online_pay',), 'seller_comm', ('online_pay', 'payment_uuid',),'adress')}),
        ("Доставка", {'fields': ( ('delivery', 'delivery_summ',), 'delivery_adress',)}),
        ("Физическое лицо", {'fields': (('person', 'phone', 'email'), 'comment',)}),
        ("Юридическое лицо", {'fields': (
            ('company', 'legaladress'),
            ('inn', 'kpp',),
            ('okpo', 'bankname',),
            ('currentacc', 'corresponding', ), 'bic',
            )}),
        )




"""
ниже старые для временной совместимости
"""

class OrderedGoodsInline(admin.TabularInline):
    model = OrderedGoodsModel
    # readonly_fields = ('client', 'vcode', 'previewImage', 'name', 'quantity', 'price', 'created_date')
    extra = 0


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id','order_numer', 'phone','total', 'status')
    list_display_links = ('id','order_numer', 'phone', 'total',)
    # readonly_fields = (
    #     'id',
    #     'order_numer',
    #     'person',
    #     'legaladress',
    #     'inn',
    #     'kpp',
    #     'okpo',
    #     'bankname',
    #     'currentacc',
    #     'corresponding',
    #     'bic',
    #     'company',
    #     'phone',
    #     'email',
    #     'adress',
    #     'total',
    #     'comment'
    #     )
    list_editable = ('status',)
    inlines = (OrderedGoodsInline,)


class RequestPriceAdmin(admin.ModelAdmin):
    """ Отображение запросов на цены """

    list_display = ('id', 'completed', 'city', 'contact', 'product')
    list_display_links = ('id', 'contact', 'product')
    list_editable = ('completed',)
    readonly_fields = ('id', 'uuid', 'city', 'contact', 'product')


admin.site.register(
    CustomerModel, 
    CustomerAdmin
    )
admin.site.register(
    RequestPriceModel, 
    RequestPriceAdmin
    )
# admin.site.register(ClientModel, ClientAdmin)