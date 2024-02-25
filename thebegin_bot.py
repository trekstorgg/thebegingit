from telegram.ext import PicklePersistence, Updater, CommandHandler, MessageHandler, Filters, CallbackContext

TOKEN = '6819081129:AAGpDpi1c4UP4Duis0JGsK2vamaEcLg0b5Q'

def start(update, context):
    update.message.reply_text('Привет! Я ваш бот.')

def echo(update, context):
    update.message.reply_text(update.message.text)

def main():
    persistence = PicklePersistence('conversation_data.pkl')
    updater = Updater(TOKEN, use_context=True, persistence=persistence)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
