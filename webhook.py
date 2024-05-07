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
    url = 'http://127.0.0.1:5000'
    print(bot.set_webhook(url=url))

set()