# from django.db import models
# from django.db.models.fields import CharField
# from django_elasticsearch_dsl import Document, fields
# from django_elasticsearch_dsl.registries import registry
# from elasticsearch_dsl.field import Keyword



from catalog.models import ProductModel, ExtendedProductModel


from django_opensearch_dsl import Document
from django_opensearch_dsl.registries import registry
from django_opensearch_dsl.fields import GeoPointField


@registry.register_document
class ProductDocument(Document):
    """ OpenSearch """

    class Index:
        name = 'products'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }
        auto_refresh = True

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
    """ OpenSearch """

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
            'city',
            'shop',
            'shop_id',
            'name',
            'price',
            'quantity',
            'last_update',
        ]

    geo_point = GeoPointField()