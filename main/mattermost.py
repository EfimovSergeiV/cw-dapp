"""
Mattermost notification

<b>mattermost_notification(template, data)</b> <br />
<ul>
message_template, order_template, <br />
request_template, one_click_order_template
</ul>
"""


import requests
from django.template import Template, Context
from main.conf import BOT_TOKEN, MATTERMOST_URL, CHANNEL_ID


headers = {
    'Authorization': f'Bearer {BOT_TOKEN}',
    'Content-Type': 'application/json'
}

def send_message(channel_id, message):
    url = f'{MATTERMOST_URL}/api/v4/posts'
    payload = {
        'channel_id': channel_id,
        'message': message
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        print("Сообщение успешно отправлено!")
    else:
        print(f"Ошибка отправки сообщения: {response.status_code} - {response.text}")



# Шаблоны сообщений

templates = {

"one_click_order_template" : """
### Заказ {{ order_number }}
Магазин: **{{ shop }}**
Клиент: **{{ name }}**
Контакты: **{{ msger }} {{ contact }}**
{% if comment %}
Комментарий к заказу:
> {{ comment }}
{% endif %}

| ID            | Название           | Стоимость  | Кол-во  |
| ------------- | ------------------ | :--------: | ------: |{% for product in prods %}
| {{ product.id }} | {{ product.name }} | {{ product.price }} руб. | {{ product.quantity }} |{% endfor %}

Итог заказа: **{{ total }}** руб.

---
""",


"request_template" : """
### Запрос стоимости товара
Контакт: **{{ contact }}**
Город: **{{ city }}**

| Ид            | Название |
| ------------- | :------: |
| {{ id }}      | [{{ product }}](https://glsvar.ru/product/{{ id }}) |

---
""",


"message_template" : """
### Сообщение от клиента
Город: **{{ city }}**
Клиент: **{{ person }}**
Контакты: **{{ contact }}**
> {{ text }}

---
""",


"order_template" : """
### Заказ {{ order_number }}
Магазин: **{{ adress }}**
Клиент: **{{ person }}**
Контакты: **{{ phone }}**    **{{ email }}**
{% if comment %}
Комментарий к заказу:
> {{ comment }}
{% endif %}

| ID            | Арт.          | Название           | Стоимость | Кол-во |
| ------------- | ------------- | :----------------: | ---------:| -----: |{% for product in client_product %}
| {{ product.id }} | {{ product.vcode }} | [{{ product.name }}](https://glsvar.ru/product/{{ product.product_id }}) | {{ product.price }} руб. | {{ product.quantity }} |{% endfor %}
Итог заказа: **{{ position_total }}** руб.

---
""",
}


# Данные для сообщений для отладки

request_data = {
    'id': 145, 
    'completed': False, 
    'uuid': '72fa8530-2988-4b81-b1a0-3f6116dd8493', 
    'city': 'Псков', 
    'contact': 'WhatsApp 123456789', 
    'product': 'id: 2011 vc: F4U31SW2000 name: Fanuci Ultron Lite 2000'
}


message_data = {
    'id': 2, 
    'completed': False, 
    'uuid': '7303ec80-cb1c-45da-85b7-bb56035bb16a', 
    'city': 'Псков', 
    'person': 'Сергей Ефимов', 
    'contact': 'sys@tehnosvar.ru', 
    'theme': 'order', 
    'text': 'Перезагрузите компьютер, чтобы проверить, что Debian автоматически входит в систему и запускает Chrome в полноэкранном режиме.'
}


order_data = {
    'uuid': '215ea411-04fa-4c2a-b4bd-8cb80a83a690', 
    'order_number': 'SMO1086329', 
    'adress': 'Смоленск, ул. Посёлок Тихвинка 69, ТК "Город Мастеров" павильон №73', 
    'position_total': 47490, 
    'total': 47490, 
    'promocode': None, 
    'delivery': False, 
    'delivery_adress': 'Самовывоз', 
    'delivery_summ': None, 
    'person': 'Сергей Ефимов', 
    'phone': 'WhatsApp +79116965424', 
    'email': 'sys@tehnosvar.ru', 
    'comment': 'Пришлите пожалуста счёт на почту', 
    'company': None, 
    'legaladress': None, 
    'inn': None, 
    'kpp': None, 
    'okpo': None, 
    'bankname': None, 
    'currentacc': None, 
    'corresponding': None, 
    'bic': None,
    'client_product': [
        { "id": 145, "product_id": 2015, "vcode": "51ST04X", "name": "Маска сварщика хамелеон DIGITAL X SMART", "price": "7050", "preview_image": "http://127.0.0.1:8000/files/img/c/preview/51ST04X-1.webp", "quantity": 1 },
        { "id": 146, "product_id": 819, "vcode": "38439", "name": "Сварочная маска FUBAG OPTIMA 4-13 Visor", "price": "6270", "preview_image": "http://127.0.0.1:8000/files/img/c/preview/prodd_IPCdyfk.webp", "quantity": 2 },
        { "id": 147, "product_id": 782, "vcode": "0700000730", "name": "Сварочная маска хамелеон A30", "price": "9300", "preview_image": "http://127.0.0.1:8000/files/img/c/preview/a20-30.webp", "quantity": 3 }
    ]
}






one_click_order_data = {
    'order_number': 'PSK1297110', 
    'name': 'Сергей Ефимов', 
    'contact': '79116965424', 
    'msger': 'WhatsApp', 
    'shop': 'пос. Неёлово, ул.Юбилейная д. 5ж', 
    'comment': 'Note that the command works by creating new messages in the target channel, but preserves most of the original message metadata. Ordering is kept intact, but the messages contain new timestamps so that channel message history is not altered.', 
    'total': 570, 
    'prods': [
        {
            'prod_type': 'ext', 
            'id': 1629, 
            'name': 'Круг Е125*7 А30 P PSF, шт', 
            'price': 205, 
            'quantity': 1
            }, 
        {
            'prod_type': 'ext', 
            'id': 1630, 
            'name': 'Круг ЕНТ 125*1,6 А46 P PSF, шт', 
            'price': 120, 
            'quantity': 1
            }, 
        {
            'prod_type': 'ext', 
            'id': 1631, 
            'name': 'Круг ЕНТ 125*1,6 А46 P PSF-INOX, по нерж., шт', 
            'price': 125, 
            'quantity': 1
            }, 
        {
            'prod_type': 'ext', 
            'id': 10, 
            'name': 'КЛТ2 150 22,2 (зернистость40), шт', 
            'price': 90, 
            'quantity': 1
            }, 
        {
            'prod_type': 'ext', 
            'id': 14, 
            'name': 'Круг 1251,2 22,2 14А , шт', 
            'price': 30, 
            'quantity': 1
            }
        ]
}


# template = Template(message_template)
# template = Template(order_template)
# template = Template(request_template)
# template = Template(one_click_order_template)


def mattermost_notification(template, data):
    context = Context(data)
    template = Template(templates[template])

    rendered_string = template.render(context)
    send_message(CHANNEL_ID, rendered_string)
