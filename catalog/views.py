import random
from unicodedata import category
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from catalog.models import *
from serializers.catalog import *
from django.db.models import CharField
from django.db.models.functions import Lower
from django.db.models import Case, When

from main.models import CourceCurrency
from catalog.utils import *

from elasticsearch_dsl import Q
from catalog.documents import ProductDocument#, ProductKeywordDocument

CharField.register_lookup(Lower)

#Logs send
# from main.agent import send_alert_to_agent


class ResultsSetPagination(PageNumberPagination):
    """Ограничение пагинации"""
    page_size = 36


class CategoryView(APIView):
    """ Категории товаров """
    def get(self, request):
        cts = CategoryModel.objects.filter(level=0).filter(activated=True)
        serializer = CategoryRecursiveSerializer(cts, many=True)
        return Response(serializer.data)


class BreadCrumbView(APIView):
    """ Хлебные крошки """

    def get(self, request):
        ct = self.request.query_params.get('ct')

        if ct is not None:
            queryset = CategoryModel.objects.all()
            """
            Cannot resolve keyword 'category_id' into field. 
            Choices are: activated, children, description, id, level, lft, name, parent, parent_id, product_category, prop_ct, rght, tree_id
            """
            # Попробовать пройти циклом ( пока парсим до 3его)
            breadcrumb = []

            qs = queryset.get(id=ct)
            breadcrumb.append(qs)

            if qs.parent_id is not None:
                parent = queryset.get(id=qs.parent_id)
                breadcrumb.insert(0, parent)
                # print(parent.parent_id)
                if parent.parent_id is not None:
                    parent = queryset.get(id=parent.parent_id)
                    breadcrumb.insert(0, parent)
        
        else:
            breadcrumb = []

        serializer = BreadCrumbSerializer(breadcrumb, many=True)
        return Response(serializer.data)


class PropsNameView(ListAPIView):
    """ 
        Свойства товаров по категориям для фильтров 
        Возможно будет работать с обратной связью
    """

    serializer_class = PropsNameSerializer

    def get_queryset(self, *args, **kwargs):
        ct = self.request.query_params.get('ct')
        queryset = PropsNameModel.objects.filter(activated=True).order_by('position')

        if ct is not None:
            queryset = queryset.filter(category=ct)


        else:
            queryset = queryset.filter(category=0) # Пока кастыль

        return queryset


class BrandCategoryView(APIView):
    """ Бренды находящиеся в категории """

    def get(self, request):
        
        ct = self.request.query_params.get('ct')
        
        
        #LETS BUGFIX
        if ct == None:
            ct = 1
        childs = [ct, ]


        category = CategoryModel.objects.get(id=ct)



        qs_child = category.get_children()
        for child in qs_child:
            childs.append(child.id)

        queryset = ProductModel.objects.filter(category_id__in = childs)
        unique_brand = []


        for qs in queryset:
            try:
                if { 'id': qs.brand.id, 'brand': qs.brand.brand } not in unique_brand:
                    unique_brand.append({ 'id': qs.brand.id, 'brand': qs.brand.brand })
            except:
                pass

        return Response(unique_brand)


class ProductsPagination(PageNumberPagination):
    """
    Пагинация с изменением стоимости товара исходя из курса валют
    """

    page = 1
    page_size = 36

    def get_paginated_response(self, data):
        meta = ListProductsView.meta
        # cources_dict = ChangeCurrency.now_currency(self)
        # change_data = []
        # for product in data:
        #     # Проверяем указана общая стоимасть или конкретно по магазинам
        #     if product['only_price_status']:
        #         product = CustomUtils.make_only_price(self, product)

        #     change_product = ChangeCurrency.change_price(self, data=product, cources=cources_dict)
        #     change_data.append(change_product)

        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'meta': meta,
            'results': data
        })


class ListProductsView(ListAPIView):
    """ Список товаров """

    serializer_class = ListProductsSerializer
    pagination_class = ProductsPagination
    
    meta = { 
        "title": str(),
        "description": str(),
        "inserted": None
        }

    def get_queryset(self):
        props = dict(self.request.query_params)

        queryset = ProductModel.objects.filter(activated=True).order_by('brand__priority')
        validated_props = []

        # Добавляем потомков категории И заполняем мету
        if 'ct' in props.keys():

            category = CategoryModel.objects.get(id=props['ct'][0])
            qs_childs = category.get_children()

            self.meta["title"] = category.name
            self.meta["description"] = category.description
            
            # Вложенные категории только тут добавляем в мету
            # Очищаем мету, если потомков нет. Потому что хэшируется
            if len(qs_childs) > 0:
                self.meta["inserted"] = [{ "id": child.id, "name": child.name } for child in category.get_children()]
            else:
                self.meta["inserted"] = None


            validated_props = PropsNameModel.objects.filter(category=props['ct'][0])

            # qs_childs = category.get_children()
            for child in qs_childs:
                props['ct'].append(child.id)
                third_childs = child.get_children()
                for third_child in third_childs:
                    props['ct'].append(third_child.id)
        else:
            if 'brnd' in props.keys():
                brand = BrandProductModel.objects.get(id=props['brnd'][0])
                self.meta["title"] = brand.brand
                self.meta["description"] = brand.description


        queryset = FilterProducts.hard_filter(self, qs=queryset, props=props)
        # logs.append(len(queryset))
        queryset = FilterProducts.soft_filter(self, qs=queryset, validated_props=validated_props, props=props)
        # logs.append(len(queryset))
        queryset = FilterProducts.ordering(self, qs=queryset, props=props)
        # logs.append(len(queryset))
        # send_alert_to_agent(logs=f"'This debug:', { logs }")
        # Фильтруем верхний и нижний порог стоимости
        # .filter(prod_price__price__range=[price_min[0], price_max[0]])

        return queryset


class ProductView(APIView):
    """ Запрос одного продукта со свойствами по id """

    queryset = ProductModel.objects.filter(activated=True)
    serializer_class = ProductSerializer

    def get(self, request, pk):
        try:
            product = self.queryset.get(id=pk)
            ct = CategoryModel.objects.get(id=product.category.id)
            related = [ct.id for ct in ct.related.all()]
            serializer = self.serializer_class(product, context={'request':request})
            data = serializer.data
            data['related'] = related

            return Response(data)
        
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        




class ProductCompView(ListAPIView):
    """ Комплекты товаров со связью на существующие товары"""

    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = ProductModel.objects.filter(activated=True)
        props = dict(self.request.query_params)

        try:
            queryset = queryset.filter(id__in=props['id[]'])
        except:
            queryset = None

        return queryset



class ProdRandomView(ListAPIView):
    """ Рандомные 12 товаров """

    serializer_class = RecommendSerializer

    def get_queryset(self):
        ct = self.request.query_params.get('ct')
        queryset = ProductModel.objects.filter(activated=True).order_by("?")

        if ct is not None:
            qs_ct = queryset.filter(category_id__in=ct)
            if len(qs_ct) > 24:
                queryset = qs_ct

        last = len(queryset)

        start_list = random.randrange(0, last - 12, 1)
        end_list = start_list + 12

        return queryset[start_list:end_list]

import random
class OneRandomProductView(APIView):
    """ Возвращает один случайный товар из запрошенных категорий """

    serializer_class = ProductSerializer
    queryset = ProductModel.objects.filter(activated=True)
    cat_qs = CategoryModel.objects.all()#filter(activated=True)

    def get(self, request):
        try:
            cts = dict(self.request.query_params)
            prods = []
            print(cts['ct'], len(cts['ct']))
            for ct in cts['ct']:
                all_categories = []
                category_qs = self.cat_qs.get(id=ct)
                children_qs = [ child.id for child in category_qs.get_children() ]
                
                all_categories.append(int(ct))
                second_child_qs = self.cat_qs.filter(id__in=children_qs)
                all_categories += [ second_category.id for second_category in second_child_qs ]
                for third_child_qs in second_child_qs:
                    all_categories += [third_child.id for third_child in third_child_qs.get_children()]

                prods.append(self.queryset.filter(category_id__in=all_categories).order_by("?")[0])
            
            while len(prods) < 4:
                prods.append(self.queryset.filter(category_id__in=all_categories).order_by("?")[0])

            random.shuffle(prods)
            serializer = self.serializer_class(prods[0:4], many=True, context={'request': request})
            
            return Response(serializer.data)
        
        except KeyError:
            return Response([])
        
        except ObjectDoesNotExist:
            return Response([])


class RecommendView(APIView):
    """ Рекомендуемые товары """
    queryset = ProductModel.objects.filter(recommend=True).filter(activated=True)
    serializer_class = RecommendSerializer

    def get(self, request):
        ct = self.request.query_params.get("ct")
        if ct:
            cat_qs = self.queryset.filter(category_id=ct).order_by("?")
        
        rec_qs = self.queryset.filter(recommend=True).order_by("?")

        if len(rec_qs) < 8:
            
            cat_qs = self.queryset.order_by("?")[0:8 - len(rec_qs)]
            qs = rec_qs | cat_qs

        else:
            rec_qs = self.queryset.filter(recommend=True).order_by("?")[0:8]
            qs = rec_qs

        serializer = self.serializer_class(qs, many=True, context={'request':request})

        # cources_dict = ChangeCurrency.now_currency(self)
        # change_data = []
        # for product in serializer.data:
        #     # Проверяем указана общая стоимасть или конкретно по магазинам
        #     if product['only_price_status']:
        #         product = CustomUtils.make_only_price(self, product)

        #     change_product = ChangeCurrency.change_price(self, data=product, cources=cources_dict)
        #     change_data.append(change_product)
        return Response(serializer.data)



class NeuesView(APIView):
    """ Новые товары """

    def get(self, request):
        products = ProductModel.objects.filter(activated=True).order_by('-id')[:12]
        serializer = RecommendSerializer(products, many=True, context={'request':request})

        # products = serializer.data

        # cources_dict = ChangeCurrency.now_currency(self)
        # change_data = []
        # for product in products:
        #     # Проверяем указана общая стоимасть или конкретно по магазинам
        #     if product['only_price_status']:
        #         product = CustomUtils.make_only_price(self, product)
        #     change_product = ChangeCurrency.change_price(self, data=product, cources=cources_dict)
        #     change_data.append(change_product)

        return Response(serializer.data)


class SaleView(APIView):
    """ Товары со скидкой """

    def get(self, request):
        products = ProductModel.objects.filter(activated=True, promo=True)
        serializer = ProductSerializer(products, many=True, context={'request':request})
        return Response(serializer.data)


class ShopAdressView(APIView):
    """ Информация о магазинах """
    def get(self, request):
        shop = ShopAdressModel.objects.order_by('position')
        serializer = ShopAdressSerializer(shop, many=True)
        return Response(serializer.data)


class SearchView(APIView):
    serializer_class = SearchSerializer
    document_class = ProductDocument

    def post(self, request):
        search_query = request.data['name']
        query = Q('multi_match', query=search_query,
                fields=[
                    'vcode',
                    'name',
                    'keywords',
                ], fuzziness='auto')

        search = self.document_class.search().query(query)[0:30]
        response = search.execute()

        prods = [prod.id for prod in response ]
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(prods)])
        qs = ProductModel.objects.filter(activated=True).filter(id__in=prods).order_by(preserved)

        serializer = self.serializer_class(qs, many=True, context={'request':request})
        return Response(serializer.data)


class BrandProductView(APIView):
    """ Список брендов """

    def get(self, request):
        brands = BrandProductModel.objects.all()
        serializer = BrandProductSerializer(brands, many=True, context={'request':request})
        return Response(serializer.data)


class ListShopView(APIView):
    """ Список магазинов для сопаставления """

    def get(self, request):
        list_shops = ShopAdressModel.objects.all()
        serializer = ShopAdrSerializer(list_shops, many=True, context={'request':request})
        return Response(serializer.data)


class ListCitiesView(APIView):
    """ Список городов в которых есть магазины """

    def get(self, request):
        list_city = CityModel.objects.all()
        serializer = CitySerializer(list_city, many=True, context={'request':request})
        return Response(serializer.data)
