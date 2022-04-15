from django.core.mail import EmailMessage
from django.utils.translation import activate
from catalog.models import ShopAdressModel, ProductModel, AvailableModel, PriceModel
from main.settings import BASE_DIR
from datetime import datetime
from django.utils.safestring import mark_safe


WRITE_TO_DB = True
log_data = [
    # { "UID товара": None , "UID магазина": None, "Стоимость": None, "Количество": None, "Запись в ДБ": None }
]

def save_logging(data, statistic):
    log_path = 'logs/' + str(datetime.now()) + '.log'

    with open( str(BASE_DIR / log_path), 'w') as file:
        count = 0
        for string in data:
            count += 1
            file.write(
                mark_safe(
                    "%s. Товар: %s, Магазин: %s, Стоимость: %s, Количество: %s, Запись в ДБ: %s \n"
                    % (count, string["UID товара"], string["UID магазина"], string["Стоимость"], string["Количество"], string["Запись в ДБ"])
                )
            )
        
        log_message = EmailMessage(
                subject = "Выгрузка данных из 1С",
                body = mark_safe(
                    """
                    Статистика по текущей выгрузке:
                    Запись в базу данных (только наличие): %s

                    Выгружено данных: %s
                    Обновлённых данных: %s
                    Последний файл: %s
                    Новый файл: %s
                    Запись в БД: %s
                    """
                    % (WRITE_TO_DB, statistic["Обнаружено записей: "], statistic["Обновлённых записей: "], statistic["Последний выгруженый: "], statistic["Созданный файл: "], len(data))),
                from_email = 'shop@glsvar.ru',
                to = ['sys@tehnosvar.ru',],
            )

        log_message.attach_file(str(BASE_DIR / log_path))
        log_message.send()
        log_data.clear()


def daemon_data_uploads(updated_upload_data, statistic):
    """
     Принимает данные которые изменились относительно последней выгрузки,
     проверяет есть ли товары в базе и записывает.
    """
    qs_shop = ShopAdressModel.objects.all()
    qs_prod = ProductModel.objects.all()

    for prod_upload in updated_upload_data:

        prod_log = dict()
        prod_log['UID товара'] = prod_upload['prod_UID']
        prod_log['UID магазина'] = prod_upload['shop_UID']
        prod_log['Стоимость'] = prod_upload['price']
        prod_log['Количество'] = prod_upload['quantity']

        prod= qs_prod.filter(UID=prod_upload['prod_UID']).exists()
        if prod:
            prod = qs_prod.get(UID=prod_upload['prod_UID'])
            shop = qs_shop.filter(UID=prod_upload['shop_UID']).exists()
            if shop:
                shop = qs_shop.get(UID=prod_upload['shop_UID'])
                currency = 'RUB' if prod_upload['currency'] not in ('RUB', 'EUR', 'USD') else prod_upload['currency']
                prod_status = 'order' if prod_upload['quantity'] == 0 else 'stock'

                if WRITE_TO_DB:
                    price_update = PriceModel.objects.filter(
                        shop = shop, 
                        product = prod
                        ).update(quantity = prod_upload['quantity'], status=prod_status)
                    # avail_update = AvailableModel.objects.filter(
                    #     shop = shop,
                    #     product = prod,
                    #     ).update(quantity = prod_upload['quantity'], status = prod_status)
                else:
                    price_update = len(PriceModel.objects.filter(shop=shop, product=prod))
                    # avail_update = len(AvailableModel.objects.filter(shop=shop, product=prod))
                


                prod_log["Запись в ДБ"] = str(price_update)
                log_data.append(prod_log)

    save_logging(data=log_data, statistic=statistic)

