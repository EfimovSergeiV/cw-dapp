from django.db import models
from django.db.models.fields import CharField
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl.field import Keyword

from catalog.models import ProductModel, ExtendedProductModel


@registry.register_document
class ProductDocument(Document):
    """ Elastic """

    class Index:
        name = 'products'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = ProductModel
        fields = [
            'id',
            'vcode',
            'name',
            'keywords',
        ]


@registry.register_document
class ExtendedProductDocument(Document):
    """ Elastic """

    class Index:
        name = 'ext_products'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = ExtendedProductModel
        fields = [
            'id',
            'name',
            'shop_id',
        ]
