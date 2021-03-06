
import telebot
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import time
from apscheduler.schedulers.blocking import BlockingScheduler


PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = '1119831121:AAHb_nvYn1M5NciLJu1NX-48jMTkrPUZ0sc'
CHAT_ID = '474164495'
HEROKU_APP_NAME = 'https://zi1ch.herokuapp.com/'

# bot = telebot.TeleBot(TOKEN)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! I am a bot')

def send(update, context):
    update.send_message('@hello_min', "Daily reminder has been set! You\'ll get notified at 11 AM daily")
    update.message.reply_text("Hello")
    
    # schedule.every().day.at("12:30").do(send)
sched = BlockingScheduler()

# Runs from Monday to Friday at 11:30 (am) until 2014-07-30 00:00:00
sched.add_job(send, 'cron', day_of_week='mon-fri', hour=15, minute=7, end_date='2021-07-30')

sched.start()
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

################################

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("send", send))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://zi1ch.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()