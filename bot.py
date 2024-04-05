from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import handlers

def main():
    TOKEN = "7099265445:AAHwc-D2btRm_91n27KeG4qafkpZT8ORC30"

    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', handlers.start))
    dp.add_handler(CallbackQueryHandler(handlers.admin, pattern='admin stng'))
    dp.add_handler(CallbackQueryHandler(handlers.userfun, pattern='user obuna'))
    dp.add_handler(CallbackQueryHandler(handlers.admin_control,pattern='admin '))
    dp.add_handler(CallbackQueryHandler(handlers.teststng,pattern='answer '))
    dp.add_handler(CallbackQueryHandler(handlers.test,pattern='test '))
    dp.add_handler(MessageHandler(Filters.regex(r'^admin\+'),handlers.addadmin))
    dp.add_handler(MessageHandler(Filters.regex(r'^admin\-'),handlers.deladmin))
    dp.add_handler(MessageHandler(Filters.regex(r'^obuna\+'),handlers.add_obuna))
    dp.add_handler(MessageHandler(Filters.regex(r'^obuna\-'),handlers.del_obuna))
    dp.add_handler(MessageHandler(Filters.regex(r'^test\+'),handlers.addtest))
    dp.add_handler(MessageHandler(Filters.regex(r'send'),handlers.reklama))
    dp.add_handler(MessageHandler(Filters.regex(r'$'),handlers.check_answer))





    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
    