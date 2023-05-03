from django.contrib import admin
from django.urls import path

from content.views import *


urlpatterns = [
    path('widebanners/', WideBannersView.as_view()),
    path('mainbanner/', MainBannerView.as_view()),
    path('mpromob/', MainPromoBannerView.as_view()),
    path('certificate/', FooterFileView.as_view()),
    path('votes/', VotesView.as_view()),
    path('reviews/', ReviewsView.as_view()),
    path('reviews/<int:pk>/', ReviewView.as_view()),
    path('random-reviews/', RandomReviewsView.as_view()),
    path('article/<int:pk>/', ArticleView.as_view()),
]