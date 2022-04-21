from django.contrib import admin
from django.urls import path

from content.views import *


urlpatterns = [
    path('mainbanner/', MainBannerView.as_view()),
    path('mpromob/', MainPromoBannerView.as_view()),
    path('certificate/', FooterFileView.as_view()),
    path('votes/', VotesView.as_view()),
]