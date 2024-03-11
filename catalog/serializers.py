from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from catalog.models import (
    CategoryModel,
    ProductModel,
)


class CategoryRecursiveSerializer(serializers.ModelSerializer):
    """MPTT категории с потомками"""
    name = serializers.CharField()
    inserted = serializers.ListField(child=RecursiveField(), source='get_children')

    class Meta:
        model = CategoryModel
        fields = ('id','name', 'image', 'level', 'inserted', 'related')


class ProductSerializer(serializers.ModelSerializer):
    """ Сериализатор товаров """
    
    class Meta:
        model = ProductModel
        fields = '__all__'


