import time
import random
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.template.loader import get_template, render_to_string

#### FIX ME ( Im double )

keytodata = {}

class Verification():

    """ Присваиваем проверочный код данным """

    # def check_date(created_data):
    #     max_time = datetime.now() - timedelta(hours=1)
    #     if created_data > max_time:
    #         print("old")
    #     else:
    #         print("new")

    def get_code(data):
        """ Присваиваем данным проверочный код """
        verification_code = random.randrange(10000, 19999)
        keytodata[verification_code] = data
        return verification_code

    def get_user(verification_code):
        if verification_code in keytodata:
            user = keytodata.pop(verification_code)
            return user
        else:
            return None


class SugnUpMails():
    """ Уведомления по электронной почте """

    def send_code(email, verification_code):
        """ Отправка кода верификации для товара""" 
        
        html_content = render_to_string('signup_vcode.html', {'verification_code': verification_code})

        send_mail(
            'Подтвердите регистрацию',
            message=html_content,
            from_email= 'shop@glsvar.ru',
            recipient_list= [email],
            fail_silently=False,
            html_message=html_content
            )

    def send_notice(email, data):
        """ Рассылка уведомлений о успешной регистрации """
        html_content = render_to_string('signup_notice.html', {
            'username': data['username']
        })
        send_mail(
            'Пользователь ' + str(data['username']) + ' успешно зарегистрирован',
            message = html_content,
            from_email = 'shop@glsvar.ru',
            recipient_list = email,
            fail_silently = False,
            html_message = html_content
            )