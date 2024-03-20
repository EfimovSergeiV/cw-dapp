from re import search
from warnings import filters
from django.contrib import admin
from django.template.loader import render_to_string
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from user.models import *


class ProfileModelInline(admin.StackedInline):
    model = ProfileModel
    can_delete = False
    verbose_name_plural = 'Профиль пользователя'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileModelInline,)


class LikeProdAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user')
    list_display_links = ('id', 'product', 'user')
    list_filter = ('user',)
    search_fields = ('user', 'product',)


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'grade', 'visible')
    list_display_links = ('id', 'product', 'user', 'grade',)
    list_editable = ('visible',)
    search_fields = ('user', 'product',)
    list_filter = ('user',)
    readonly_fields = ('product', 'user', 'grade', )


class FeedBackAdmin(admin.ModelAdmin):
    list_display = ('id' , 'completed', 'city', 'uuid','person', 'theme',)
    list_display_links = ('id' , 'completed', 'person', 'theme',)
    search_fields = ('person', )
    list_filter = ('theme', )
    readonly_fields = ('person', 'theme', 'contact', 'text',)


from catalog.models import ProductModel
from django.db.models import Case, When
class UserWatcherAdmin(admin.ModelAdmin):

    def preserved(self, prods):
        return Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(prods)])

    def parse_prods(self, instance):
        products = instance.prods
        if products:
            qs_prods = ProductModel.objects.filter(id__in = products["viewed"] + products["like"] + products["comp"])
            
            data = render_to_string('admin_prods.html', {
                "viewed": qs_prods.filter(id__in = products["viewed"]).order_by(self.preserved(products["viewed"])),
                "like": qs_prods.filter(id__in = products["like"]).order_by(self.preserved(products["like"])),
                "comp": qs_prods.filter(id__in = products["comp"]).order_by(self.preserved(products["comp"])),
                
            })
            return data
        else:
            return 'В истории ничего нет'
    
    parse_prods.short_description = 'Товары в сессии'


    list_display = ('tmp_id', 'createdAt', 'updatedAt', )
    list_display_links = ('tmp_id', 'createdAt', 'updatedAt',  )
    readonly_fields = ('prods', 'parse_prods',  'createdAt', 'updatedAt', )
    fieldsets = (
        ("Активность", {'fields': (( 'createdAt', 'updatedAt', ),)}),
        ("Сессия", {'fields': (('parse_prods'),)}),
        )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(SubscriberModel)
admin.site.register(FeedBackModel, FeedBackAdmin)

admin.site.register(UserWatcherModel, UserWatcherAdmin)

# admin.site.register(LikeProdModel, LikeProdAdmin)
# admin.site.register(ProductReviewModel, ProductReviewAdmin)