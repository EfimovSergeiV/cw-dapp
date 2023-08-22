"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from main.views import *
from main import settings
from django.conf.urls.static import static

urlpatterns = [
    # Applications
    path('', MainPageView.as_view()),
    path('a/', admin.site.urls),
    path('c/', include('catalog.urls')),
    path('o/', include('orders.urls')),
    path('c/', include('content.urls')),
    path('u/', include('user.urls')),
    path('s/', include('services.urls')),
    path('f/', include('forum.urls')),
    path('sber/', include('sber.urls')),
    path('dreamkas/', include('dreamkas.urls')),

    # Main logic
    path('auth/', AuthTokenView.as_view()),             # Авторизация
    path('logout/', LogoutView.as_view()),             # Авторизация
    path('signup/', SignUpView.as_view()),              # Подробная регистрация
    path('subscriebe/', SubscriebeUserView.as_view()),  # Быстрая регистрация
    # path('u/change/', ChangeUserView.as_view()),      # Изменить инфо пользователя
    path('u/reset/', RestoreUserPassword.as_view()),    # Восстановить пароль
    path('u/profile/', UserProfileView.as_view()),      # Информация о пользователе
    path('location/', ReturnClientLocation.as_view()),  # Местонахождение
    path('coordinates/', CoordinateProcessingView.as_view()),
    path('nearshop/', NearShop.as_view()),              # Ближайший магазин
    path('version/', VersionControlView.as_view()),     # Версия фронтенд приложения
    path('myip/', ClientIpAdressView.as_view()),        # Возращает IP адрес
    path("getsignature/", signature_generator, name='signature_generator'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))

admin.site.site_header = 'Администрирование приложения'
admin.site.index_title = 'Интернет магазин Главный сварщик'
admin.site.site_title = 'Администрирование приложения'