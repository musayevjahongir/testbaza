from telegram import Bot
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.environ.get('TOKEN')

bot = Bot(token=TOKEN)

def get_info():
    print(bot.get_webhook_info())


def delete():
    print(bot.delete_webhook())


def set():
    url = 'https://jahon0306.pythonanywhere.com/'
    print(bot.set_webhook(url=url))

set()