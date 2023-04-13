from django.contrib import admin
from django.urls import path, re_path
from catalog.views import *


urlpatterns = [
    path('shops/', ShopAdressView.as_view()),
    path('ct/', CategoryView.as_view()),
    path('recommend/', RecommendView.as_view()),
    path('neues/', NeuesView.as_view()),
    path('sale/', SaleView.as_view()),
    path('search/', SearchView.as_view()),
    path('listshop/', ListShopView.as_view()),
    path('listcities/', ListCitiesView.as_view()),
    path('brands/', BrandProductView.as_view()),
    path('prod/<int:pk>/', ProductView.as_view()),
    
    re_path('related/', OneRandomProductView.as_view()),
    # re_path('analogs/', OneRandomProductView.as_view()),

    re_path('breadcrumb/', BreadCrumbView.as_view()),
    re_path('prods/', ListProductsView.as_view()),
    re_path('props/', PropsNameView.as_view()),
    re_path('ctbrand/', BrandCategoryView.as_view()),
    re_path('random/', ProdRandomView.as_view()),
    re_path('comp/', ProductCompView.as_view()),

    # re_path('test/', TestProperty.as_view()),
]