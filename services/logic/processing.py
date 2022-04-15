from typing import Counter, NewType
from django.core.mail import EmailMessage
from django.db.models.fields.related import RECURSIVE_RELATIONSHIP_CONSTANT
from django.utils.translation import activate
from catalog.models import ShopAdressModel, ProductModel, AvailableModel, PriceModel
from main.settings import BASE_DIR
from datetime import datetime
from django.utils.safestring import mark_safe
import time

import json
from services.logic.prod_update import WRITE_TO_DB


class DataProcessing():
    """ 1C DATA UPLOAD PROCESSING """
    def __init__(self, data):
        """ Инициализируем данные из новой выгрузки """
        self.data = data


    def comp_data(self):
        """ Записываем новые данные и возвращаем те, что изменились с момента последней выгрузки.
        Если старых данных нет, то просто записываем и возвращаем новые данные. """
        try:
            with open(str(BASE_DIR / 'uploads/data.json'), encoding='utf-8') as file:
                o_data = json.load(file)
                new_data = []
                for cursor in self.data:            # Сортируем данные и перезаписываем файл
                    if dict(cursor) not in o_data:
                        new_data.append(dict(cursor))

            with open(str(BASE_DIR / 'uploads/data.json'), 'w', encoding="utf-8") as file:
                json.dump(self.data, file, ensure_ascii=False,)
                
            return new_data

        except FileNotFoundError:
            with open(str(BASE_DIR / 'uploads/data.json'), 'w', encoding="utf-8") as file:
                json.dump(self.data, file, ensure_ascii=False,)
            return self.data


    def logging(self, writed_data=None, count_data=None):
        """ Логирование выгрузки """

        with open(str(BASE_DIR / 'uploads/data.log'), 'w', encoding="utf-8") as log_file:
            for writed in writed_data:
                log_file.write('\n' + writed + '\n')
                for shop in writed_data[writed]:
                    log_file.write(shop + '\n')


        log_message = EmailMessage(
            subject = "Выгрузка данных из 1С",
            body = f"Товаров: { len(writed_data) } \nЗаписей: { count_data } из { len(self.data) }",
            from_email = 'shop@glsvar.ru',
            to = ['sys@tehnosvar.ru',],
        )
        log_message.attach_file(str(BASE_DIR / 'uploads/data.log'))
        log_message.send()
        print(f"{ len(writed_data) } из { len(self.data) }")


    def write_data(new_d):
        """ Проверка и запись новых данных """
        qs_price = PriceModel.objects.all()
        writed = {}
        count = 0

        for cursor in new_d:
            price = qs_price.filter(shop__UID=cursor['shop_UID'], product__UID=cursor['prod_UID'])
            if price:
                count += 1
                currency = 'RUB' if cursor['currency'] not in ('RUB', 'EUR', 'USD') else cursor['currency']
                prod_status = 'order' if cursor['quantity'] == 0 else 'stock'
                
                if price[0].verified:
                    price.update(price=cursor['price'], currency=currency, quantity = cursor['quantity'], status=prod_status)

                product = f"ID: { price[0].product.id } Т-Р: { price[0].product.name }"
                if product not in writed.keys():
                    writed[product] = list()
                    writed[product].append(
                        f"СТ-ТЬ: { price[0].price } -> { cursor['price'] }  НАЛ-Е: { cursor['quantity'] }  МАГ-Н: { price[0].shop.adress }")
                else:
                    writed[product].append(
                        f"СТ-ТЬ: { price[0].price } -> { cursor['price'] }  НАЛ-Е: { cursor['quantity'] }  МАГ-Н:  { price[0].shop.adress }")
        return { "writed": writed, "count": count }


""" Управляющая функция """
def start_process(data_uploads):

    print('START PROCESS')

    pull_data = DataProcessing(data_uploads)
    n_data = pull_data.comp_data()

    if n_data:
        result = DataProcessing.write_data(n_data)
        if result['writed']:
            pull_data.logging(writed_data=result['writed'], count_data=result['count'])
        else:
            print('NOT WRITED DATA')
            pass
    else:
        print("NOT UNIQUE NDATA")
        pass



