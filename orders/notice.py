from django.core.mail import send_mail
from django.template.loader import get_template, render_to_string


class OrderMails():
    """ Уведомления по электронной почте """

    def send_code(email, verification_code):
        """ Отправка кода верификации для товара""" 
        # print(verification_code)
        html_content = render_to_string('order_vcode.html', {'verification_code': verification_code})

        send_mail(
            'Подтвердите заказ',
            message=html_content,
            from_email= 'shop@glsvar.ru',
            recipient_list= [email],
            fail_silently=False,
            html_message=html_content
            )

    def send_notice(email, data):
        """ Рассылка уведомлений о успешной покупке """
        # print('SUCCESS', email, data)
        html_content = render_to_string('order_notice.html', {
            'order_number': data['order_number'],
            'person': data['person'],
            'phone': data['phone'],
            'email': data['email'],
            'adress': data['adress'],
            
            # Доставка
            'delivery': data['delivery'],
            'delivery_summ': data['delivery_summ'],
            'delivery_adress': data['delivery_adress'],

            # Юр.Лицо доп форма
            "company": data["company"],
            "legaladress": data["legaladress"],
            "inn": data["inn"],
            "kpp": data["kpp"],
            "okpo": data["okpo"],
            "bankname": data["bankname"],
            "currentacc": data["currentacc"],
            "corresponding": data["corresponding"],
            "bic": data["bic"],

            'comment': data['comment'],
            'total': data['total'],
            'client_product': data['client_product']
        })
        send_mail(
            'Заказ на сумму ' + str(data['total']) + 'RUB успешно принят',
            message = html_content,
            from_email = 'shop@glsvar.ru',
            recipient_list = email,
            fail_silently = False,
            html_message = html_content
            )
