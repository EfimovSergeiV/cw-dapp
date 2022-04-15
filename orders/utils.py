import random

orders = {}


def get_position_summ(products):
    """ Вычисление суммы по позициям заказа """
    total = 0
    for product in products:
        total += product['price'] * product['quantity']
    return total

# class OrdersData():
#     """ Отсеиваем клиентов с неправильно указанной почтой """

#     def add_order(order_data):
#         """ Добавляем заказ во временное хранище и возвращаем назначенный код подтверждения """
#         verification_code = random.randrange(10000, 19999)
#         orders[verification_code] = order_data
#         return verification_code

#     def get_order(verification_code):
#         """ Возвращаем заказ по если ключ совпал """
#         if verification_code in orders:
#             order = orders.pop(verification_code)
#             return order
#         else:
#             return None


# написать счётчик для удаления первого элемента ,если он есть по таймеру.