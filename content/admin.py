from django.contrib import admin
from content.models import *



@admin.register(MainBannerModel)
class MainBannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'description')
    list_display_links = ('id', 'name', 'image', 'description')


@admin.register(WideBannersModel)
class WideBannersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'activated')
    list_display_links = ('id', 'name',)
    list_editable = ('activated',)


@admin.register(WorkingShopsModel)
class WorkingShopsAdmin(admin.ModelAdmin):
    list_display = ('id', 'google_table_url', 'created_at', 'activated',)
    list_display_links = ('id', 'google_table_url', 'created_at',)
    list_editable = ('activated',)