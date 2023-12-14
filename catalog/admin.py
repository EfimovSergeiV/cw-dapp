from django.contrib import admin
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin
from catalog.models import *


# Генератор
import string
import random

def gen(size=4, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'parent','activated')
    list_editable = ('activated', )
    fieldsets = (
        (None, {'fields': (('parent', 'activated', ),)}),
        (None, {'fields': ('description',)}),
        (None, {'fields': ('related',)}),
    )
    

class BrandProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'brand', 'image')
    list_display_links = ('id', 'brand', 'image')

class ShopArdessAdmin(admin.ModelAdmin):
    list_display = ('position', 'adress', 'phone')
    list_display_links = ( 'adress', 'phone')
    list_editable = ('position',)
    ordering = ('position',)


##### FOR USER FILTERS
class PropOpsModel(admin.TabularInline):
    model = PropOpsModel
    extra = 0

"""Отображение товара в админ панели"""
class AvailableInline(admin.TabularInline):
    model = AvailableModel
    extra = 0


class ProductDocumentInline(admin.TabularInline):
    model = DocumentModel
    list_display = ('name', 'doc','description',)
    fieldsets = (
        (None, {'fields': ('name', 'doc', 'description',)}),
        )
    extra = 0


class ExternalLinkInline(admin.TabularInline):
    model = ExternalLinkModel
    list_display = ('name', 'url', 'description',)
    fieldsets = (
        (None, {'fields': ('name', 'url', 'description',)}),
        )
    extra = 0


class ProductImageInline(admin.TabularInline):
    model = ProductImageModel

    readonly_fields = ('preview', )
    def preview(self, obj):
        return mark_safe('<img style="margin-right: -10vh" src="/files/%s" alt="Нет изображения" width="160" height="auto" />' % (obj.image))
    preview.short_description = 'Изображение'
    fieldsets = (
        (None, {'fields': ('preview', 'image')}),
        )
    extra = 0

class ProductSetInline(admin.TabularInline):
    model = ProductSetModel
    readonly_fields = ('set_link', )
    def set_link(self, obj):
        return mark_safe(
            '''
            <a style="background-color: #777777; padding: 5px; color: #fff; border-radius: 3px;" href="/a/catalog/productsetmodel/%s"
            target="blank"><b>↪️Подробное редактирование</b></a>
            '''
            % (obj.id))
    set_link.short_description = 'Подробное редактирование'
    fieldsets = (
        (None, {'fields': ( 'set_link', 'vcode', 'name', 'price', 'activated')}),
        )
    extra = 0

class ProdCompInline(admin.TabularInline):
    model = ProductCompModel
    extra = 0


class PropStrInline(admin.TabularInline):
    model = PropStrModel
    readonly_fields = ('get_qname', )
    def get_qname(self, obj):
        try:
            prop = PropsNameModel.objects.get(name=obj.name)
            return mark_safe(
                '''
                <p style="background-color: #777777; margin-top: -4px; padding: 2px; color: #fff; border-radius: 3px;">%s</p>
                '''
                % (prop.prop_alias))
        except:
            return mark_safe(
                '''
                <p style="background-color: #777777; margin-top: -4px; padding: 2px; color: #fff; border-radius: 3px;">Err</p>
                ''')
    get_qname.short_description = 'Алиас'
    # ordering = ('qname',)
    fieldsets = (
        (None, {'fields': ( 'name', 'value', 'qname', 'get_qname', 'qvalue',)}),
        )
    extra = 0


class ProductKeywordsInline(admin.TabularInline):
    model = ProductKeywordModel
    extra = 0


##### ОСНОВНЫЕ НАСТРОЙКИ ТОВАРОВ
class ProductAdmin(admin.ModelAdmin):

    def preview(self, obj):
        return mark_safe('<img style="margin-right: -10vh" src="/files/%s" alt="Нет изображения" width="160" height="auto" />' % (obj.preview_image))
    preview.short_description = 'Изображение'

    """
    def rec(self, obj):
        ERRORS:
            <class 'catalog.admin.ProductAdmin'>: (admin.E121) The value of 'list_editable[0]' refers to 'rec',
             which is not an attribute of 'catalog.ProductModel'.

            return obj.recommend
        recommend.short_description = 'Рек'    
    """

    readonly_fields = ('preview', )
    list_display = ('id', 'vcode', 'name', 'only_price', 'currency', 'activated', 'status',) #'recommend',
    list_display_links = ('id', )
    search_fields = ('id', 'vcode', 'name', 'UID',)
    list_filter = ('brand', 'show_more', 'recommend', 'created_date', 'activated', 'category',)
    list_editable = ('only_price', 'activated', 'status')
    ordering = ('id',)
    inlines = (
        # ProductKeywordsInline,
        # AvailableInline,
        # ProductSetInline,
        # ProdCompInline, 
        ProductImageInline, 
        PropStrInline, 
        ProductDocumentInline, 
        ExternalLinkInline
        )
    sortable_by = ('id')
    fieldsets = (
        ("Отображение на сайте", {'fields': (('activated', 'show_more', 'recommend',), ('category', 'brand'), ( 'preview', 'preview_image',))}),
        ("Информация о товаре", {'fields': (('name', 'vcode', 'UID', 'rating'), 'description', 'keywords',)}),
        ("Стоимость и наличие", {'fields': (('only_price_status', 'promo'), ('only_price', 'currency', 'status', ), ('discount',),)}),
        ("Сопутствующие категории", {'fields': (('related',),)}),
        )

##### НАЗВАНИЯ СВОЙСТВ ДЛЯ ФИЛЬТРОВ
class PropNameAdmin(admin.ModelAdmin):
    readonly_fields = ('get_alias', )
    def get_alias(self, obj):
        if len(obj.prop_alias) == 0:
            prop = gen()
            # Не думаю что будет выдавать всегда уникальные
            exist_alias = PropsNameModel.objects.filter(prop_alias=prop)
            if exist_alias:
                prop = gen()
        else:
            prop = '🦝'           

        return mark_safe(
            '''
            <p style="background-color: #888888; padding: 4px; color: #fff; border-radius: 3px;">%s</p>
            '''
            % (prop))
    get_alias.short_description = 'Возможный алиас'

    list_display = ('id', 'name', 'prop_alias', 'propwidget', 'position', 'activated',)
    list_display_links = ('id', 'name',)
    ordering = ('id',)
    search_fields = ('name', 'prop_alias', )
    list_editable = ('prop_alias', 'propwidget', 'position', 'activated',)
    list_filter = ('category',)
    fieldsets = (
        ("ОТОБРАЖЕНИЕ В СПИСКЕ ФИЛЬТРОВ", {'fields': ( 
            ( 'position', 'activated', ), 
            'name', ('prop_alias', 'get_alias', ), 
            'description', 
            ( 'category', 'propwidget', ))}),
        )
    inlines = (PropOpsModel,)


class PriceAdmin(admin.ModelAdmin):
    # change_list_template = "custom_price.html"
    list_display = ('id', 'vcode_product', 'product', 'price', )
    ordering = ('id',)
    search_fields = ('product__name', 'product__vcode', 'product__id')
    list_editable = ['price', ]
    list_filter = ('product__brand', 'product__activated',)

class AvailableAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'quantity')
    list_display_links = ('id', 'status', 'quantity')


class ProductSetAdmin(admin.ModelAdmin):
    readonly_fields = ('preview_set', )
    def preview_set(self, obj):
        return mark_safe('<img style="margin-right: -10vh" src="/files/%s" alt="Нет изображения" width="160" height="auto" />' % (obj.preview_image))
    preview_set.short_description = ''

    list_display = ('id', 'vcode', 'product', 'price', 'activated')
    list_display_links = ('id', 'vcode', 'product',)
    list_editable = ('price', 'activated', )
    search_fields = ( 'vcode', 'product', )

    fieldsets = (
        ("Информация о товаре", {'fields': (('name', 'vcode',),('UID', 'activated',), 'description')}),
        ('↪️', {'fields': (('product', ), ('preview_set', 'preview_image',))}),
        )


class CatalogFileAdmin(admin.ModelAdmin):
    readonly_fields = ('path_file', )
    def path_file(self, obj):
        return 'https://api.glsvar.ru/files/' + str(obj.file)
    path_file.short_description = 'Путь до файла'
        
    list_display = ('id', 'name', 'path_file')
    list_display_links = ('id', 'name',)
    fieldsets = (
        ("Файлы каталога", {'fields': (('name', 'file',), 'path_file', 'description')}),
    )
    search_fields = ('id', 'name')


admin.site.register(BrandProductModel, BrandProductAdmin)
admin.site.register(CityModel)
admin.site.register(CategoryModel, CategoryAdmin)
admin.site.register(ProductSetModel, ProductSetAdmin)
admin.site.register(ShopAdressModel, ShopArdessAdmin)
admin.site.register(ProductModel, ProductAdmin)
admin.site.register(PropsNameModel, PropNameAdmin)
admin.site.register(CatalogFileModel, CatalogFileAdmin)


# admin.site.register(ProductFeedbackModel) ### FeedBack
# admin.site.register(PriceModel, PriceAdmin)
# admin.site.register(AvailableModel, AvailableAdmin)