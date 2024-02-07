import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter

from csv import list_dialects
from django.contrib import admin
from django.utils.safestring import mark_safe
from dreamkas.models import  DreamkasProductModel, ReceiptsStatusModel   # DreamkasPriceModel,


class ProductAdmin(admin.ModelAdmin):
    """ Форматирование товара """
    list_display = ('association', 'name', 'id', 'createdAt','updatedAt',)
    list_display_links = ('id', 'association', 'name')
    fieldsets = (
        ("", {'fields': (
                'isMarked', 
                ('name', 'association',),
                ('id',),
                ('type', 'quantity',),
                ('tax',),
                ('createdAt', 'updatedAt',),
            )},
        ),
    )
    readonly_fields = ('createdAt', 'updatedAt',)
    search_fields = ('id', 'association', 'name',)


class ReceiptsStatusAdmin(admin.ModelAdmin):
    """ Статусы фискализации чеков """

    def get_check(self, obj):
        """ Представление чека """
        data = obj.cash_receipt
        json_data = json.dumps(data, sort_keys=True, indent=2, ensure_ascii=False)
        formatter = HtmlFormatter(style='colorful')
        response = highlight(json_data, JsonLexer(), formatter)
        style = "<style>" + formatter.get_style_defs() + "</style><br>"
        return mark_safe(style + response)

    get_check.short_description = 'JSON data'

    readonly_fields = ('get_check', )
    list_display = ('id', 'externalId', 'createdAt', 'status',)
    list_display_links = ('id', 'externalId',)
    fieldsets = (
        ("Данные фискализации", {'fields': (('id', 'externalId',), ('createdAt', 'status',),)}),
        ("Данные чека", {'fields': (('get_check',),)}),
    )
    # readonly_fields = ('id', 'externalId', 'createdAt', 'status',)
    search_fields = ('id', 'externalId',)


# admin.site.register(DreamkasProductModel, ProductAdmin)
# admin.site.register(ReceiptsStatusModel, ReceiptsStatusAdmin)
