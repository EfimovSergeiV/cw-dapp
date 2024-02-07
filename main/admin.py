from django.contrib import admin
from main.models import *


class IdentificationServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'service_url', 'service_key', 'service_statistic', 'activated')
    list_display_links = ('id', 'service_url', 'service_key', 'service_statistic',)


# admin.site.register(CourceCurrency)
# admin.site.register(DeleviryServiceModel)
# admin.site.register(VersionControlModel)
# admin.site.register(UserIdentificationServiceModel, IdentificationServiceAdmin)