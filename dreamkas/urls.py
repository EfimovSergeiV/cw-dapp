from django.urls import path, re_path

from dreamkas.views import *



urlpatterns = [
    # WebHoocks
    re_path('receipts/', UpdateReceiptsStatusWebhook.as_view())
]
