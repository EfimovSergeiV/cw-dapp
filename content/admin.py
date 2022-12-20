from django.contrib import admin
from content.models import *


class MainBannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'description')
    list_display_links = ('id', 'name', 'image', 'description')


class SecondBannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'description')
    list_display_links = ('id', 'name', 'image', 'description')


class MainPromoBannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'activated')
    list_display_links = ('id', 'name', 'image',)
    sortable_by = ('id')
    list_editable = ('activated',)
    fieldsets = (
        ("Настройки", {'fields': (( 'name', 'tposition', 'activated',),)}),
        ("Файлы и изображение", {'fields': (('file_pdf', 'image', 'link'),)}),
        ("Описание", {'fields': (('description', 'dposition',),)}),
        )


class SecondPromoBannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'description')
    list_display_links = ('id', 'name', 'image', 'description')


class VoteInline(admin.TabularInline):
    """ Вывод вариантов голосований в админке """

    model = VotesAnswersModel
    readonly_fields = ('voted',)
    extra = 0

class VotesAdmin(admin.ModelAdmin):
    """ Вывод опросов в админке """

    list_display = ('id', 'vote', 'is_active')
    list_display_links = ('id', 'vote', 'is_active')
    inlines = [VoteInline]

admin.site.register(VotesInterviewedModel)


admin.site.register(FooterFileModel)
admin.site.register(MainBannerModel, MainBannerAdmin)
admin.site.register(VotesModel, VotesAdmin)
admin.site.register(MainPromoBannerModel, MainPromoBannerAdmin)
admin.site.register(WideBannersModel, )
# admin.site.register(SecondPromoBannerModel, SecondPromoBannerAdmin)
# admin.site.register(SecondBannerModel, SecondBannerAdmin)
