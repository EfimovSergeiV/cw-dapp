from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
import json, requests
from html.parser import HTMLParser

# import pandas as pd
# from time import sleep



BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass



url = 'https://aurora-online.ru/catalog/welding/?print=1&&'
html = requests.get(url).text
devices = []

# class MyHTMLParser(HTMLParser):
#     def __init__(self):
#         super().__init__()
#         self.h1_content = False

#     def handle_starttag(self, tag, attrs):
#         # Если тег <h1>, устанавливаем флаг в True
#         if tag == 'h1':
#             self.h1_content = True

#     def handle_data(self, data):
#         # Если флаг установлен в True, сохраняем содержимое <h1>
#         if self.h1_content:
#             # print("Содержимое тега <h1>: ", data)
#             if len(data) > 3:
#                 devices.append(data)
#             self.h1_content = False



class MyHTMLParser(HTMLParser):
    """ h1, td, div """

    def __init__(self):
        super().__init__()
        self.h1_content = False
        self.div_content = False
        self.td_content = False


    def handle_starttag(self, tag, attrs):
        """ Реагируем на тег """

        if tag == 'h1':
            self.h1_content = True

        if tag == 'div':
            self.div_content = True

        if tag == 'td':
            self.td_content = True


    def handle_data(self, data):
        """ Записываем """

        # if self.h1_content:
        #     if len(data) > 3:
        #         devices.append(data)
        #     self.h1_content = False

        if self.div_content:
            if len(data) > 3:
                devices.append(data)
            self.div_content = False

        if self.td_content:
            if len(data) > 3:
                devices.append(data)
            self.td_content = False



parser = MyHTMLParser()
parser.feed(html)

count = 0
for device in devices:
    count += 1

    # if count % 3:
    #     v_code = str(device).split()[-1]
    #     print(f'{ v_code }')

    # else:
    #     print(f'{ device }')

    print(f'\n{ device }')

