"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from main.conf import *
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


### THIS DOUBLE
REST_FRAMEWORK = {  
    # "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'main.models.BearerAuthentication',
        # "rest_framework.authentication.SessionAuthentication",
        # "dj_rest_auth.utils.JWTCookieAuthentication",

    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_elasticsearch_dsl',
    'debug_toolbar',
    'corsheaders',
    'mptt',
    'easy_thumbnails',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'main.apps.MainConfig',
    'user.apps.UserConfig',
    'content.apps.ContentConfig',
    'catalog.apps.CatalogConfig',
    'orders.apps.OrdersConfig',
    'services.apps.ServicesConfig',
    'sber.apps.SberConfig',
    'dreamkas.apps.DreamkasConfig',
    # Auth & social auth # THIS CRASHING SITE
    # 'django.contrib.sites',
    # "dj_rest_auth",
    # "allauth",
    # "allauth.account",
    # "dj_rest_auth.registration",
    # "allauth.socialaccount",
    # "allauth.socialaccount.providers.google",   
]

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'SCOPE': [
#             'profile',
#             'email',
#         ],
#         'AUTH_PARAMS': {
#             'access_type': 'online',
#         }
#     }
# }

# # Disable email verification since this is just a test.
# # If you want to enable it, you'll need to configure django-allauth's email confirmation pages
# SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
# SOCIALACCOUNT_EMAIL_REQUIRED = False

# REST_USE_JWT = True

# SITE_ID = 1

# from datetime import timedelta

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
#     'ROTATE_REFRESH_TOKENS': True, # IMPORTANT
#     'BLACKLIST_AFTER_ROTATION': True, # IMPORTANT
#     'UPDATE_LAST_LOGIN': True,
# }

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


THUMBNAIL_ALIASES = {
    '': {
        'small': {'size': (60, 40), 'crop': True},
        'preview': {'size': (235, 177), 'crop': True},
        'full': {'size': (640, 480), 'crop': True},
    },
}

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_L10N = True
USE_TZ = False


# Elasticsearch
# https://django-elasticsearch-dsl.readthedocs.io/en/latest/settings.html

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200'
    },
}


# ЛОМАЕТ АВТОРИЗАЦИЮ:
#
# REST_FRAMEWORK = {
#     # Only enable JSON renderer by default.
#     'DEFAULT_RENDERER_CLASSES': [
#         'rest_framework.renderers.JSONRenderer',
#     ],
# }


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = '/files/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'files/')
MPTT_ADMIN_LEVEL_INDENT = 40
