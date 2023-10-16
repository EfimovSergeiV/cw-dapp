from django.core.management.base import BaseCommand, CommandError
from pathlib import Path
from bot.bot import Bot
from main.conf import mailagent_bot_token

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Command(BaseCommand):
    args = ''
    help = ''
    
    def handle(self, *args, **options):
        pass



target = "@AoLG-JRaQb24KBu3ZwI"

f = {'file data': open('./img.jpg', 'rb')}
h = { "token": mailagent_bot_token, "chatId": target, } 


bot = Bot(token=mailagent_bot_token)


def image_cb():
    bot.send_file(
        chat_id= target,
        file = open('./img.jpg', 'rb')
    )
image_cb()
