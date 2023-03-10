from main.models import CourceCurrency
# from main.agent import send_alert_to_agent

class CustomUtils:
    """ Утилитки """

    def make_only_price(self, data):
        """ Ставим общую стоимость на товары """
        prod_price = []
        for price in data.pop('prod_price'):
            dict_price = dict(price)
            dict_price['price'] = data['only_price']
            dict_price['currency'] = data['currency']
            prod_price.append(dict_price)

        data['prod_price'] = prod_price

        return data


class ChangeCurrency:
    """ Изменение стоимости товара исходя из стоимости валюты """

    def now_currency(self) -> dict:
        """
        Возвращает установленные валюты:
        { "EUR": 94.4, "USD": 83.7 , "RUB": 1 }
        """
        cources = CourceCurrency.objects.all()
        cources_dict = {}
        for cource in cources:
            cources_dict[cource.name] = cource.cource

        return cources_dict


    def change_price(self, data, cources):
        """ Подменяет prod_price на пересчитанный """
        prod_price = []

        for price in data.pop('prod_price'):
            dict_price = dict(price)

            summ = dict_price['price'] * cources[dict_price['currency']]
            dict_price['price'] = int(summ)
            dict_price['currency'] = 'RUB'

            prod_price.append(dict_price)

        data['prod_price'] = prod_price

        return data



class FilterProducts:
    """ Логики отфильтровки товаров по запросу """

    def hard_filter(self, qs, props):
        """ Фильтр по категориям и брендам """

        # print(f'\nHARD FILTER: {props}\n')

        filters = {
            'ct': 'category_id__in',
            'brnd[]': 'brand__id__in',
            'brnd': 'brand__id__in',        # <- Err
        }

        params = {}
        for item in props:
            if item in filters.keys():
                params[filters[item[0:4]]] = props[item]

        qs = qs.filter(**params)
        # print(f'\nLEN QUERYSET{len(qs)}\n')
        return qs

    def soft_filter(self, qs, validated_props, props):
        """ Фильтр по параметрам товара """
        list_props = {}

        for prop in validated_props:
            list_props[prop.prop_alias] = prop.propwidget

        for prop in props:
            if prop[0:4] in list_props:
                if 'false' not in props[prop]:
                    if list_props[prop[:4]] == 'value':
                        qs = qs.filter(
                            propstrmodel__qname=prop[0:4], 
                            propstrmodel__qvalue__in=props[prop]
                        )

                    if list_props[prop[:4]] == 'range':
                        qs = qs.filter(
                            propstrmodel__qname='jnzs', 
                            propstrmodel__qvalue__range=props[prop][0].split('-')
                            )

        return qs

    def ordering(self, qs, props):
        """ Ordering по товарам\n
        Дописать чтобы норм работало и валютами
        """
        ordering = {
            'Date'      : '-id',
            'LowPrice'  : 'prod_price__price',
            'HighPrice' : '-prod_price__price',
            'Rating'    : '-rating',
        }

        if 'by' in props.keys():
           qs = qs.order_by(ordering[props['by'][0]]).distinct()

        return qs
