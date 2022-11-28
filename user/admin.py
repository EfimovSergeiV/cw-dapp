from re import search
from warnings import filters
from django.contrib import admin
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


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(SubscriberModel)
admin.site.register(FeedBackModel, FeedBackAdmin)
admin.site.register(LikeProdModel, LikeProdAdmin)
admin.site.register(ProductReviewModel, ProductReviewAdmin)