from flask import Flask,request
from telegram import Update, Bot
from telegram.ext import CommandHandler,MessageHandler,Dispatcher,Filters, CallbackQueryHandler
import handlers
from dotenv import load_dotenv
import os

load_dotenv()  # .env faylni yuklash

TOKEN = os.environ.get('TOKEN')  # TOKEN ni .env faylidan olish

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, None, workers=0)

app = Flask(__name__)

@app.route("/webhook",methods=["GET","POST"])
def main():
    if request.method=="GET":
        return "runing"
    if request.method=="POST":
        body = request.get_json()
        update = Update.de_json(body, bot)
        
        dp.add_handler(CommandHandler('start', handlers.start))
        dp.add_handler(CallbackQueryHandler(handlers.admin, pattern='admin stng'))
        dp.add_handler(CallbackQueryHandler(handlers.userfun, pattern='user obuna'))
        dp.add_handler(CallbackQueryHandler(handlers.admin_control,pattern='admin '))
        dp.add_handler(CallbackQueryHandler(handlers.teststng,pattern='answer '))
        dp.add_handler(CallbackQueryHandler(handlers.test,pattern='test '))
        dp.add_handler(CallbackQueryHandler(handlers.balltest,pattern='ball +'))
        dp.add_handler(MessageHandler(Filters.regex(r'^admin\+'),handlers.addadmin))
        dp.add_handler(MessageHandler(Filters.regex(r'^admin\-'),handlers.deladmin))
        dp.add_handler(MessageHandler(Filters.regex(r'^obuna\+'),handlers.add_obuna))
        dp.add_handler(MessageHandler(Filters.regex(r'^obuna\-'),handlers.del_obuna))
        dp.add_handler(MessageHandler(Filters.regex(r'^test\+'),handlers.addtest))
        dp.add_handler(MessageHandler(Filters.regex(r'send'),handlers.reklama))
        dp.add_handler(MessageHandler(Filters.regex(r'$'),handlers.check_answer))
        dp.process_update(update)

        return {"message","ok"}
    
if __name__ == "__main__":
    app.run(debug=True)
