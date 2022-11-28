"""
***
Mail Agent for notifications from glsvar website

"""

from bot.bot import Bot
from django.conf import settings
from main.conf import mailagent_bot_token, mail_contacts
from django.template.loader import render_to_string


bot = Bot(token=mailagent_bot_token)


def send_alert_to_agent(
        order=None, 
        payment=None, 
        message=None, 
        logs=None, 
        pricerequest=None,
        status=None,
        oth_status=None,
        ):
    """ Отправка активностей в агент """

    if order:
        chats_to_send_notifications = mail_contacts['admins']
        text_to_send = render_to_string('magent.html', {
            'uuid': order['uuid'],
            'order_number': order['order_number'],
            'adress': order['adress'],
            'person': order['person'],
            'phone': order['phone'],
            'email': order['email'],
            'total': order['total'],
            'delivery': order['delivery'],
            'delivery_adress': order['delivery_adress'],
            'comment': order['comment'],
            'client_product': order['client_product'],
        })

    if payment:
        chats_to_send_notifications = mail_contacts['admins']

        text_to_send = f"""
<pre>
Заказ оплачен онлайн
Номер заказа: { payment['order_number'] }
Сумма оплаты: { payment['total']}
</pre>
<a href="https://3dsec.sberbank.ru/payment/merchants/sbersafe_sberid/payment_ru.html?mdOrder={ payment['payment_uuid'] }">Проверить</a> 
"""

    if message:
        chats_to_send_notifications = mail_contacts['channel']

        text_to_send = f"""
<pre>
Город: { message['city'] }
Клиент: { message['person'] }
Контакты: { message['contact'] }
</pre>

Сообщение: 
{ message['text'] }

---
<a href="https://api.glsvar.ru/u/message_close/{ message['uuid'] }">Ответил</a>
"""

    if logs:
        chats_to_send_notifications = ['efimovsergeipr@mail.ru',]
        print(logs)
        text_to_send = f"{ logs }"

    if pricerequest:
        chats_to_send_notifications = mail_contacts['channel']
        text_to_send = f"""
<pre>
Запрос клиента на стоимость товара
Контакт клиента: { pricerequest['contact'] }
Город клиента: { pricerequest['city'] }
</pre>

Товар: 
{ pricerequest['product'] }

---
<a href="https://api.glsvar.ru/o/pricerequest_close/{ pricerequest['uuid'] }">Ответил</a>
"""


    if status:
        chats_to_send_notifications = mail_contacts['channel']

        text_to_send = f"""
<pre>
Заказ: { status['order'] }
Получил статус: { status['status'] }
</pre>
"""

    if oth_status:
        chats_to_send_notifications = mail_contacts['channel']

        text_to_send = f"""
<pre>
Клиент: { oth_status['client'] }
Помечен как проработанный
</pre>
"""

    for chat in chats_to_send_notifications:
        bot.send_text(chat_id=chat, text=text_to_send, parse_mode="HTML")
